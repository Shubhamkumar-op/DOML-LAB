# Experiment-13: RAG LLM Quality, Drift, Context Relevance, and Guardrail Monitoring

## Aim
Build a Retrieval-Augmented Generation (RAG) system and monitor its output similarity, context relevance, simple guardrails, and potential drift with Evidently and a Streamlit dashboard.

## Project description
This practical uses a small disaster-management knowledge base. LangChain and FAISS retrieve the two most relevant documents for a question. Gemma 3 4B running locally through Ollama generates an answer from the retrieved context. Sentence-transformer embeddings and cosine similarity are used to compare reference answers with current and synthetic-drift answers. Evidently creates HTML drift reports, and simple validation rules check context-word overlap and answer length.

## Requirements
- Python and VS Code
- Git
- Ollama installed and running
- Local Ollama model `gemma3:4b`

## Files
```text
RAG_LLM_Monitoring/
├── app.py
├── requirements.txt
└── README.md
```
The app generates `rag_llm_drift.html`, `rag_llm_synthetic_drift.html`, and `rag_llm_monitoring_outputs.csv` after a successful run.

## Installation
Open a terminal in this folder and install dependencies:
```powershell
python -m pip install -r requirements.txt
```
Check that Gemma is installed:
```powershell
ollama list
```
The output should include `gemma3:4b`. Ollama needs to be running, with its local API available at `http://127.0.0.1:11434`.

## Run the dashboard
```powershell
python -m streamlit run app.py
```
Open the local URL printed in the terminal, normally `http://localhost:8501`, then click **Run RAG Monitoring**.

## Workflow
1. Load a small disaster-management knowledge base.
2. Build a FAISS vector index with `all-MiniLM-L6-v2` embeddings.
3. Retrieve the top two documents for each query.
4. Ask local Gemma to answer using the retrieved context.
5. Generate reference, current, and synthetic-drift answer batches.
6. Embed the answers and calculate cosine similarity.
7. Run Evidently `DataDriftPreset` to create HTML reports for current and synthetic-drift batches.
8. Apply simple guardrails: context-word overlap and a maximum answer length of fewer than 150 words.
9. Display answers, guardrail results, similarity metrics, and report downloads in Streamlit.

## Outputs and screenshots
Capture screenshots of:
1. Streamlit dashboard after the run completes.
2. Retrieved context and Gemma answers.
3. Guardrail table and failed checks (if any).
4. Similarity metrics and cosine-similarity matrix.
5. Evidently report opened in a browser.

## Important limitations
This is a classroom demonstration with a small knowledge base and three queries per batch. The context-overlap check is only a heuristic; it does not prove that an answer is factually correct or free of hallucinations. Cosine similarity is a proxy for semantic change, not an objective quality score. Larger representative datasets and stronger evaluation methods are needed for production monitoring.

## Result
A local RAG pipeline using Gemma and FAISS was implemented with output monitoring, cosine similarity, Evidently reports, and simple guardrails, with metrics and results shown in Streamlit.
