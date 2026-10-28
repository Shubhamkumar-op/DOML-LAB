# Experiment-12: LLM Output Drift Monitoring using Gemma, Evidently and Streamlit



## Aim



To deploy a small Large Language Model (LLM) pipeline, monitor its outputs for semantic drift, compare reference and current outputs, and visualize monitoring metrics using Evidently and Streamlit.



## Project Description



This project uses the locally installed Gemma 3 4B model through Ollama to generate text outputs. Sentence Transformers converts the generated outputs into embeddings. Cosine similarity is used to compare current outputs against reference outputs. Evidently generates HTML reports, while Streamlit provides an interactive monitoring dashboard.



## Technologies Used



- Python

- Ollama

- Gemma 3 4B (`gemma3:4b`)

- Sentence Transformers (`all-MiniLM-L6-v2`)

- Evidently

- Streamlit

- Pandas

- NumPy

- Scikit-learn

- Requests



## Project Structure



```text

LLM\_Drift\_Monitoring/

├── app.py

├── requirements.txt

├── README.md

├── llm\_drift\_dashboard.html

├── llm\_drift\_dashboard\_synthetic.html

└── llm\_monitoring\_outputs.csv

```



The HTML reports and CSV file are generated after running the monitoring dashboard.



## Installation



### 1. Install the required libraries



Open the terminal in this project folder and run:



```powershell

python -m pip install -r requirements.txt

```



### 2. Verify the local Gemma model



Check the available Ollama models:



```powershell

ollama list

```



The output should include:



```text

gemma3:4b

```



Make sure Ollama is running before starting the application.



\## Run the Dashboard



From the project folder, execute:



```powershell

python -m streamlit run app.py

```



Open the local Streamlit URL shown in the terminal, usually:



`http://localhost:8501`



Click \*\*Run LLM Drift Monitoring\*\* to start the experiment.



## Monitoring Workflow



1\. Generate reference text outputs using Gemma.

2\. Generate current production-style outputs using different prompts.

3\. Generate synthetic drift outputs using significantly different prompts.

4\. Convert all generated outputs into semantic embeddings.

5\. Calculate cosine similarity between current and reference embeddings.

6\. Compare embedding distributions using Evidently.

7\. Display generated text and monitoring metrics in the Streamlit dashboard.

8\. Save Evidently reports as HTML files and generated outputs as a CSV file.



## Generated Reports



The application creates:



- `llm\_drift\_dashboard.html` — Evidently report comparing reference and current output embeddings.

- `llm\_drift\_dashboard\_synthetic.html` — Evidently report comparing reference and synthetic drift embeddings.

- `llm\_monitoring\_outputs.csv` — CSV containing reference, current, and synthetic drift outputs.



The HTML reports can be opened in a web browser.



## Metrics



The dashboard displays average cosine similarity for current and synthetic drift outputs.



Higher cosine similarity generally indicates greater semantic similarity between output sets. Lower similarity may indicate a semantic shift.



Evidently also compares the statistical distributions of embedding features between reference and current data.



## Screenshots



Add screenshots showing:



1. The Streamlit dashboard.

2. Reference, current, and synthetic drift outputs.

3. Cosine similarity metrics and the similarity matrix.

4. Evidently report generation.

5. The generated HTML report opened in a browser.



## Result



A local LLM monitoring pipeline was implemented using Gemma 3 4B, Ollama, Sentence Transformers, Evidently, and Streamlit. The application generates text outputs, compares their semantic embeddings, calculates cosine similarity, and creates HTML reports for drift monitoring.



## Conclusion



This experiment demonstrates a basic approach to monitoring LLM output changes over time. Gemma generates the outputs, Sentence Transformers creates embeddings, cosine similarity compares output sets, Evidently produces drift reports, and Streamlit presents the results interactively.



## Limitations



This is a small laboratory demonstration using only three prompts in each group. Cosine similarity and embedding distribution changes are indicators rather than definitive proof of output-quality drift. Larger and more representative datasets are needed for reliable production monitoring.

