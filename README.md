# 🚨 Operation Ditwah: Crisis Intelligence Pipeline
![Tests](https://github.com/janithush/Operation_Ditwah-Crisis_Intelligence_Pipeline/actions/workflows/tests.yml/badge.svg)

An LLM-powered crisis intelligence pipeline that turns unstructured disaster reports and citizen messages into structured, actionable data — built for a flood/disaster relief scenario across Sri Lankan districts (Colombo, Gampaha, Kandy, Kalutara, Galle, Matara, Ratnapura, Kegalle, Anuradhapura).

The pipeline handles five distinct engineering challenges: intent classification, model stability testing, multi-step reasoning for logistics, cost/token governance, and schema-validated data extraction.

---

## 💡 Overview

During an active disaster response, responders are flooded with unstructured messages — some are genuine rescue calls, some are supply requests, some are just noise. This project automates that triage using a chain of prompting techniques (few-shot, CoT, ToT) layered on top of a resilient, multi-provider LLM client. It:

- **Classifies** incoming messages by district, intent, and priority
- **Stress-tests** reasoning outputs for consistency across temperature settings
- **Plans logistics** for a single rescue boat across competing incident priorities
- **Manages cost/token budgets** by detecting and summarizing oversized inputs
- **Extracts structured records** from raw news feed text into validated, exportable reports

---

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **Package Management:** `uv` (project uses a standard `pyproject.toml`)
- **LLM Providers:** `google-genai` (Gemini), `openai` (GPT/o-series), `groq` (Llama)
- **Schema Validation:** `pydantic` (used for structured extraction models)
- **Data Handling:** `pandas`, `openpyxl` (Excel report generation)
- **Tokenization:** `tiktoken`
- **Dev Tooling:** `ipython`, `jupyter`, `python-dotenv`, `langsmith`

---

## 📂 Project Structure

```text
├── data/
│   ├── Sample Messages.txt     # Raw messages for few-shot classification
│   ├── Scenarios.txt           # CoT stability test scenarios
│   ├── Incidents.txt           # Incident data for logistics scoring
│   └── News Feed.txt           # Raw feed for schema extraction
├── notebooks/
│   └── 05_mini_project_0.ipynb # Main pipeline notebook (Parts 1–5)
├── output/
│   ├── classified_messages.xlsx
│   └── flood_report.xlsx
├── utils/
│   ├── llm_client.py           # Multi-provider client, retries, token guards
│   ├── router.py                # Model routing (pick_model, should_use_reasoning_model)
│   ├── config_loader.py         # Retry/backoff config defaults
│   ├── token_utils.py           # Token counting, context-fit, usage reconciliation
│   ├── json_utils.py            # Auto-repairing JSON parser + schema validation
│   ├── prompts.py               # Central prompt template registry
│   └── logging_utils.py         # CSV run logging + cost estimation
├── pyproject.toml
└── .env                         # API keys (not committed)
```

> Note: `router.py` and `config_loader.py` are referenced throughout `llm_client.py` and the notebook but weren't included in the reviewed files — structure above reflects their expected role based on usage.

---

## 🚀 Pipeline Features

### Part 1 — Few-Shot Message Classification
Loads `Sample Messages.txt`, applies the `few_shot.v1` prompt template with four labeled examples, and classifies each message into `District | Intent | Priority`. Results are saved to `output/classified_messages.xlsx`.

### Part 2 — Stability Experiment (Temperature Stress Test)
Runs `cot_reasoning.v1` prompts against `Scenarios.txt` at `temperature=0.0` ("Safe Mode") and `temperature=1.0` ("Chaos Mode", 3 runs) to evaluate output consistency of the reasoning model.

### Part 3 — The Logistics Commander (CoT + ToT)
- **Step A (CoT):** Scores each incident in `Incidents.txt` (1–10) using a fixed rule set — age extremes, rescue need, medical need.
- **Step B (ToT):** Explores three routing strategies (Greedy, Speed, Logistics) for a single rescue boat departing from Ragama, then selects the optimal path under travel-time constraints.

### Part 4 — The "Budget Keeper" (Token Economics)
Counts tokens on incoming messages via `count_messages_tokens`. Messages exceeding a 150-token limit trigger `overflow_summarize.v1`, which compresses the content and extracts the sender's core intent before further processing.

### Part 5 — News Feed Extraction Pipeline
Defines a `CrisisEvent` Pydantic model (`district`, `flood_level_meters`, `victim_count`, `main_need`, `status`). Each line of `News Feed.txt` is passed through `json_extract.v1`, parsed and validated with `parse_json_with_pydantic`, and valid records are saved to `output/flood_report.xlsx`.

---

## 🧠 Architecture Highlights

**Auto-Repairing JSON Parser (`json_utils.py`)**
`safe_parse_json` chains extraction and repair: it first tries a direct parse, then pulls JSON out of markdown/mixed text via `extract_json`, and finally applies `repair_json` to fix trailing commas, unquoted keys, single quotes, and stray comments — before handing off to Pydantic for schema validation.

**Multi-Provider LLM Client & Routing (`llm_client.py`, `router.py`)**
`LLMClient` provides one interface across OpenAI, Gemini, and Groq, with automatic exponential backoff + jitter on 429/5xx/timeout errors, pre-call token estimation, context-overflow handling via `fit_within_context`, and reconciliation of estimated vs. actual token usage per call. Model selection (general/reasoning/extraction tasks) is delegated to `router.py`.

**Usage Logging & Cost Estimation (`logging_utils.py`)**
Every call is logged to `logs/runs.csv` with timestamp, latency, retry count, backoff time, and token counts. `estimate_cost` maps provider/model pairs to a per-1M-token pricing table to produce a cost estimate per call, with `get_log_summary` aggregating totals via pandas.

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Operation_Ditwah-Crisis_Intelligence_Pipeline
```

### 2. Environment Setup (using `uv`)
```bash
uv venv
uv sync
```

### 3. Configure API Keys
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY="your_openai_key_here"
GEMINI_API_KEY="your_gemini_key_here"
GROQ_API_KEY="your_groq_key_here"
```

### 4. Run the Pipeline
Open and run `notebooks/05_mini_project_0.ipynb` sequentially (Parts 1–5) in Jupyter or VS Code.


## 🧪 Testing
Unit tests are implemented using `pytest` to ensure the reliability of core data extraction components. 

To run the tests locally:
```bash
pytest