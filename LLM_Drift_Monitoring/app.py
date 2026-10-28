import streamlit as st
import pandas as pd
import numpy as np
import requests

from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from evidently import Report
from evidently.presets import DataDriftPreset


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="LLM Drift Monitoring",
    page_icon="📊",
    layout="wide"
)

st.title("LLM Output Drift Monitoring")
st.write(
    "Monitor Gemma LLM outputs, detect semantic drift, "
    "and generate Evidently reports."
)

# ---------------- CONFIGURATION ----------------

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma3:4b"

OUTPUT_DIR = Path(__file__).resolve().parent


# ---------------- LOAD EMBEDDING MODEL ----------------

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- GENERATE LLM OUTPUTS ----------------

def generate_outputs(prompts):
    outputs = []

    for prompt in prompts:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "seed": 42,
                    "num_predict": 40
                }
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()
        generated_text = result.get("response", "").strip()

        if not generated_text:
            raise RuntimeError(
                f"Gemma returned an empty response for: {prompt}"
            )

        # Keep prompt and generated response together
        outputs.append(
            f"{prompt} {generated_text}".strip()
        )

    return outputs


# ---------------- CREATE EMBEDDINGS ----------------

def create_embeddings(texts, embedding_model):
    return embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )


# ---------------- EMBEDDINGS DATAFRAME ----------------

def embeddings_to_dataframe(embeddings):
    columns = [
        f"embedding_{i}"
        for i in range(embeddings.shape[1])
    ]

    return pd.DataFrame(
        embeddings,
        columns=columns
    )


# ---------------- COSINE SIMILARITY ----------------

def calculate_similarity(current_embeddings, reference_embeddings):
    similarities = cosine_similarity(
        current_embeddings,
        reference_embeddings
    )

    average_similarity = float(np.mean(similarities))

    return similarities, average_similarity


# ---------------- EVIDENTLY REPORT ----------------

def generate_evidently_report(
    reference_embeddings,
    current_embeddings,
    report_filename
):
    reference_df = embeddings_to_dataframe(
        reference_embeddings
    )

    current_df = embeddings_to_dataframe(
        current_embeddings
    )

    report = Report([
        DataDriftPreset()
    ])

    snapshot = report.run(
        current_data=current_df,
        reference_data=reference_df
    )

    report_path = OUTPUT_DIR / report_filename

    snapshot.save_html(str(report_path))

    return report_path


# ---------------- MAIN DASHBOARD ----------------

st.sidebar.header("Monitoring Settings")
st.sidebar.write("LLM Model: `gemma3:4b`")
st.sidebar.write("Embedding Model: `all-MiniLM-L6-v2`")
st.sidebar.write("Drift Tool: Evidently")


st.info(
    "Click the button below to generate reference, current, "
    "and synthetic-drift outputs using your local Gemma model."
)


if st.button(
    "Run LLM Drift Monitoring",
    type="primary"
):

    # Check whether Ollama is running
    try:
        check = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=5
        )
        check.raise_for_status()

        installed_models = [
            item.get("name", "")
            for item in check.json().get("models", [])
        ]

        if not any(
            name == MODEL_NAME
            or name.startswith("gemma3:4b")
            for name in installed_models
        ):
            st.error(
                "gemma3:4b was not found in Ollama. "
                "Run `ollama list` and check the model name."
            )
            st.stop()

    except requests.RequestException as error:
        st.error(
            "Cannot connect to Ollama. Make sure Ollama is running."
        )
        st.code(str(error))
        st.stop()

    try:
        with st.spinner(
            "Generating Gemma outputs and monitoring drift. "
            "This may take a few minutes..."
        ):

            # Step 1: Reference prompts
            reference_prompts = [
                "Disaster response in urban areas:",
                "Predicting the impact of floods on communities:",
                "Summarize the earthquake damages in 2025:"
            ]

            # Step 2: Current production prompts
            current_prompts = [
                "Disaster response in rural areas:",
                "Predicting floods in coastal cities:",
                "Summarize the earthquake damages in 2026:"
            ]

            # Step 3: Synthetic drift prompts
            drifted_prompts = [
                "Disaster response during a pandemic:",
                "Impact of hurricanes on agriculture:",
                "Effects of volcanic eruptions in 2026:"
            ]

            # Generate outputs using Gemma
            reference_texts = generate_outputs(
                reference_prompts
            )

            current_texts = generate_outputs(
                current_prompts
            )

            drifted_texts = generate_outputs(
                drifted_prompts
            )

            # Load embedding model
            embedding_model = load_embedding_model()

            # Step 4: Convert outputs to embeddings
            reference_embeddings = create_embeddings(
                reference_texts,
                embedding_model
            )

            current_embeddings = create_embeddings(
                current_texts,
                embedding_model
            )

            drifted_embeddings = create_embeddings(
                drifted_texts,
                embedding_model
            )

            # Step 5: Calculate similarities
            similarities, average_similarity = (
                calculate_similarity(
                    current_embeddings,
                    reference_embeddings
                )
            )

            drifted_similarities, drifted_similarity = (
                calculate_similarity(
                    drifted_embeddings,
                    reference_embeddings
                )
            )

            # Step 6: Generate Evidently reports
            current_report_path = generate_evidently_report(
                reference_embeddings,
                current_embeddings,
                "llm_drift_dashboard.html"
            )

            synthetic_report_path = generate_evidently_report(
                reference_embeddings,
                drifted_embeddings,
                "llm_drift_dashboard_synthetic.html"
            )

            # Save outputs and metrics to a CSV file
            output_df = pd.DataFrame({
                "reference_output": reference_texts,
                "current_output": current_texts,
                "synthetic_drift_output": drifted_texts
            })

            output_df.to_csv(
                OUTPUT_DIR / "llm_monitoring_outputs.csv",
                index=False
            )

    except Exception as error:
        st.error(
            "Monitoring could not be completed. "
            "Check the error details below."
        )
        st.exception(error)
        st.stop()

    # ---------------- DISPLAY RESULTS ----------------

    st.success(
        "LLM output monitoring completed successfully!"
    )

    st.header("1. Drift Monitoring Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Reference Outputs",
            len(reference_texts)
        )

    with col2:
        st.metric(
            "Current Output Similarity",
            f"{average_similarity:.3f}"
        )

    with col3:
        st.metric(
            "Synthetic Drift Similarity",
            f"{drifted_similarity:.3f}"
        )

    st.caption(
        "Cosine similarity ranges from -1 to 1. Values closer "
        "to 1 indicate greater semantic similarity. A lower "
        "value may indicate a change in output content."
    )

    # ---------------- OUTPUT SECTIONS ----------------

    st.header("2. Reference Outputs")

    for index, text in enumerate(reference_texts, start=1):
        with st.expander(f"Reference Output {index}"):
            st.write(text)

    st.header("3. Current Production Outputs")

    for index, text in enumerate(current_texts, start=1):
        with st.expander(f"Current Output {index}"):
            st.write(text)

    st.header("4. Synthetic Drift Outputs")

    for index, text in enumerate(drifted_texts, start=1):
        with st.expander(f"Drifted Output {index}"):
            st.write(text)

    # ---------------- SIMILARITY MATRIX ----------------

    st.header("5. Cosine Similarity Matrix")

    similarity_df = pd.DataFrame(
        similarities,
        columns=[
            f"Reference {i + 1}"
            for i in range(len(reference_texts))
        ],
        index=[
            f"Current {i + 1}"
            for i in range(len(current_texts))
        ]
    )

    st.dataframe(
        similarity_df.round(3),
        use_container_width=True
    )

    st.write("Average current similarity:", round(
        average_similarity, 3
    ))

    st.write("Average synthetic drift similarity:", round(
        drifted_similarity, 3
    ))

    # ---------------- EVIDENTLY DASHBOARDS ----------------

    st.header("6. Evidently Drift Reports")

    st.write(
        "Evidently compares the statistical distributions of "
        "reference embeddings against current or drifted embeddings."
    )

    st.success(
        f"Current report saved: {current_report_path.name}"
    )

    st.success(
        f"Synthetic drift report saved: {synthetic_report_path.name}"
    )

    st.download_button(
        label="Download Current Drift Report",
        data=current_report_path.read_bytes(),
        file_name=current_report_path.name,
        mime="text/html"
    )

    st.download_button(
        label="Download Synthetic Drift Report",
        data=synthetic_report_path.read_bytes(),
        file_name=synthetic_report_path.name,
        mime="text/html"
    )

    # ---------------- DOWNLOAD GENERATED OUTPUTS ----------------

    output_csv_path = OUTPUT_DIR / "llm_monitoring_outputs.csv"

    st.download_button(
        label="Download LLM Outputs CSV",
        data=output_csv_path.read_bytes(),
        file_name=output_csv_path.name,
        mime="text/csv"
    )

    st.header("7. Interpretation")

    if drifted_similarity < average_similarity:
        st.warning(
            "Synthetic drift outputs are less similar to the "
            "reference set. This may indicate a semantic shift."
        )
    else:
        st.info(
            "Synthetic drift outputs were not less similar to "
            "the reference set in this run. Check the Evidently "
            "report and embeddings before drawing conclusions."
        )

    st.caption(
        "This is a small lab demonstration using three examples "
        "per group. Similarity is a proxy for semantic change, "
        "not a definitive measurement of LLM quality or drift."
    )

else:
    st.warning(
        "Monitoring has not run yet. Click "
        "'Run LLM Drift Monitoring' to start the experiment."
    )