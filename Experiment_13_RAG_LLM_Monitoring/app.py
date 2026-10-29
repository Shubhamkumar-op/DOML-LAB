import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import streamlit as st
from evidently import Report
from evidently.presets import DataDriftPreset
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="RAG LLM Quality and Drift Monitoring", page_icon="🔎", layout="wide")
st.title("RAG LLM Quality and Drift Monitoring")
st.caption("Gemma 3 4B · Ollama · FAISS retrieval · Evidently · Guardrails")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
MODEL_NAME = "gemma3:4b"
OUTPUT_DIR = Path(__file__).resolve().parent
DOCUMENTS = [
    "Floods cause severe damage to infrastructure, homes, roads, and agriculture.",
    "Earthquakes can destroy buildings, damage roads, and lead to injuries and loss of life.",
    "Wildfires spread rapidly in dry forest areas and threaten wildlife, homes, and air quality.",
    "Disaster management involves preparedness, rescue, relief, recovery, and rehabilitation.",
    "Early warning systems help communities prepare for hazards and reduce disaster impacts.",
]
REFERENCE_QUERIES = [
    "What are effects of floods?",
    "How do earthquakes impact humans?",
    "What is disaster management?",
]
CURRENT_QUERIES = [
    "Impact of floods on cities?",
    "Explain earthquake damage?",
    "Role of disaster response teams?",
]
DRIFT_QUERIES = [
    "Space disasters and satellites?",
    "Ocean storms impact?",
    "Alien invasion effects?",
]

@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def build_vector_store():
    embedder = load_embedding_model()
    return FAISS.from_texts(DOCUMENTS, embedder)

def check_ollama():
    response = requests.get(OLLAMA_TAGS_URL, timeout=5)
    response.raise_for_status()
    names = [item.get("name", "") for item in response.json().get("models", [])]
    if not any(name == MODEL_NAME or name.startswith(MODEL_NAME) for name in names):
        raise RuntimeError(f"Model {MODEL_NAME} was not found. Run `ollama list` and check the model name.")

def rag_pipeline(query, vector_store):
    documents = vector_store.similarity_search(query, k=2)
    context = "\n".join(doc.page_content for doc in documents)
    prompt = (
        "You are a disaster-information assistant. Answer the question using only the context below. "
        "If the context does not contain enough information, say that the provided context is insufficient. "
        "Do not invent facts. Keep the answer concise.\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION:\n{query}\n\nANSWER:"
    )
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False,
              "options": {"temperature": 0.2, "seed": 42, "num_predict": 100}},
        timeout=300,
    )
    response.raise_for_status()
    answer = response.json().get("response", "").strip()
    if not answer:
        raise RuntimeError("Gemma returned an empty answer.")
    return {"query": query, "context": context, "answer": answer}

def check_relevance(context, answer):
    stop_words = {"this", "that", "with", "from", "they", "them", "have", "what", "when", "where", "which", "about", "into", "there", "their", "then", "also", "only", "using", "provided", "context", "answer"}
    context_words = {word.lower() for word in re.findall(r"[A-Za-z]{4,}", context) if word.lower() not in stop_words}
    answer_words = {word.lower() for word in re.findall(r"[A-Za-z]{4,}", answer) if word.lower() not in stop_words}
    return len(context_words & answer_words) >= 1

def check_length(answer):
    return len(answer.split()) < 150

def apply_guardrails(record):
    relevant = check_relevance(record["context"], record["answer"])
    length_ok = check_length(record["answer"])
    return {
        "Query": record["query"],
        "Context Relevant": relevant,
        "Length OK": length_ok,
        "Possible Hallucination Risk": not relevant,
        "Answer Word Count": len(record["answer"].split()),
    }

def embed_answers(records, embedder):
    return embedder.embed_documents([record["answer"] for record in records])

def embedding_dataframe(embeddings):
    return pd.DataFrame(embeddings, columns=[f"embedding_{i}" for i in range(embeddings.shape[1])])

def save_evidently_report(reference_embeddings, current_embeddings, filename):
    report = Report([DataDriftPreset()])
    snapshot = report.run(
        current_data=embedding_dataframe(current_embeddings),
        reference_data=embedding_dataframe(reference_embeddings),
    )
    output_path = OUTPUT_DIR / filename
    snapshot.save_html(str(output_path))
    return output_path

def run_monitoring():
    check_ollama()
    vector_store = build_vector_store()
    embedder = load_embedding_model()
    progress = st.progress(0, text="Generating reference RAG outputs...")
    reference_records = [rag_pipeline(query, vector_store) for query in REFERENCE_QUERIES]
    progress.progress(30, text="Generating current RAG outputs...")
    current_records = [rag_pipeline(query, vector_store) for query in CURRENT_QUERIES]
    progress.progress(60, text="Generating synthetic drift outputs...")
    drift_records = [rag_pipeline(query, vector_store) for query in DRIFT_QUERIES]
    progress.progress(75, text="Calculating embeddings and similarity...")
    reference_embeddings = np.asarray(embed_answers(reference_records, embedder))
    current_embeddings = np.asarray(embed_answers(current_records, embedder))
    drift_embeddings = np.asarray(embed_answers(drift_records, embedder))
    current_similarity = float(np.mean(cosine_similarity(current_embeddings, reference_embeddings)))
    drift_similarity = float(np.mean(cosine_similarity(drift_embeddings, reference_embeddings)))
    progress.progress(85, text="Generating Evidently reports...")
    current_report = save_evidently_report(reference_embeddings, current_embeddings, "rag_llm_drift.html")
    drift_report = save_evidently_report(reference_embeddings, drift_embeddings, "rag_llm_synthetic_drift.html")
    rows = []
    for batch_name, records in [("reference", reference_records), ("current", current_records), ("synthetic_drift", drift_records)]:
        for record in records:
            rows.append({"batch": batch_name, **record, **apply_guardrails(record)})
    outputs_df = pd.DataFrame(rows)
    outputs_csv = OUTPUT_DIR / "rag_llm_monitoring_outputs.csv"
    outputs_df.to_csv(outputs_csv, index=False)
    progress.progress(100, text="Monitoring complete.")
    return {
        "reference": reference_records,
        "current": current_records,
        "drift": drift_records,
        "current_similarity": current_similarity,
        "drift_similarity": drift_similarity,
        "guardrails": pd.DataFrame([apply_guardrails(record) for record in current_records]),
        "current_report": current_report,
        "drift_report": drift_report,
        "outputs_csv": outputs_csv,
        "similarity_matrix": cosine_similarity(current_embeddings, reference_embeddings),
    }

if "monitoring_results" not in st.session_state:
    st.session_state.monitoring_results = None

with st.sidebar:
    st.header("Configuration")
    st.write(f"LLM: `{MODEL_NAME}`")
    st.write("Retriever: FAISS (top 2 documents)")
    st.write("Embeddings: all-MiniLM-L6-v2")
    st.write("Drift report: Evidently")
    st.write("Guardrails: context overlap and answer length")

if st.button("Run RAG Monitoring", type="primary"):
    try:
        with st.spinner("Running RAG queries through local Gemma. This can take a few minutes..."):
            st.session_state.monitoring_results = run_monitoring()
        st.success("RAG monitoring completed!")
    except Exception as error:
        st.error("Monitoring failed. Check that Ollama is running, Gemma is installed, and dependencies are available.")
        st.exception(error)

results = st.session_state.monitoring_results
if results:
    st.header("1. Monitoring Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Reference Queries", len(results["reference"]))
    col2.metric("Current Average Similarity", f"{results['current_similarity']:.3f}")
    col3.metric("Synthetic Drift Similarity", f"{results['drift_similarity']:.3f}")
    st.caption("Similarity is a proxy for semantic change, not a definitive measure of answer correctness or hallucination.")

    st.header("2. Reference Outputs")
    for i, record in enumerate(results["reference"], 1):
        with st.expander(f"Reference {i}: {record['query']}"):
            st.write("**Retrieved context**")
            st.write(record["context"])
            st.write("**Gemma answer**")
            st.write(record["answer"])

    st.header("3. Current Outputs")
    for i, record in enumerate(results["current"], 1):
        with st.expander(f"Current {i}: {record['query']}"):
            st.write("**Retrieved context**")
            st.write(record["context"])
            st.write("**Gemma answer**")
            st.write(record["answer"])

    st.header("4. Context and Output Guardrails")
    st.dataframe(results["guardrails"], use_container_width=True)
    failed = int((~results["guardrails"]["Context Relevant"]).sum() + (~results["guardrails"]["Length OK"]).sum())
    st.metric("Guardrail checks failed", failed)
    st.caption("These are simple heuristic checks for the lab, not a reliable factuality detector.")

    st.header("5. Synthetic Drift Outputs")
    for i, record in enumerate(results["drift"], 1):
        with st.expander(f"Drift query {i}: {record['query']}"):
            st.write("**Retrieved context**")
            st.write(record["context"])
            st.write("**Gemma answer**")
            st.write(record["answer"])

    st.header("6. Cosine Similarity Matrix")
    matrix = pd.DataFrame(results["similarity_matrix"], index=[f"Current {i}" for i in range(1, 4)], columns=[f"Reference {i}" for i in range(1, 4)])
    st.dataframe(matrix.round(3), use_container_width=True)

    st.header("7. Evidently Reports")
    st.download_button("Download current drift report", results["current_report"].read_bytes(), file_name=results["current_report"].name, mime="text/html")
    st.download_button("Download synthetic drift report", results["drift_report"].read_bytes(), file_name=results["drift_report"].name, mime="text/html")
    st.download_button("Download RAG output CSV", results["outputs_csv"].read_bytes(), file_name=results["outputs_csv"].name, mime="text/csv")
    st.info("Lower similarity or failed guardrails can indicate a potential shift or answer/context mismatch. Review the retrieved sources and report before drawing conclusions.")
else:
    st.info("Click 'Run RAG Monitoring' to retrieve documents, generate Gemma answers, check guardrails, and create Evidently reports.")
