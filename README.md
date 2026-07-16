# 🚨 Operation Ditwah: Crisis Intelligence Pipeline

An intelligent, LLM-powered data extraction and classification pipeline designed to process unstructured emergency news feeds and output structured, actionable datasets for disaster management.

## 💡 Overview

During natural disasters (like floods or landslides), critical information is often scattered across unstructured text messages, social media posts, and news feeds. This project leverages Large Language Models (LLMs) to automatically read, classify, and extract vital incident data into a highly structured format (Excel) for rapid emergency response.

The pipeline features intelligent LLM routing, strict schema validation, and built-in token budget management.

## ✨ Key Features

* **Intelligent Data Extraction:** Converts raw, noisy text into highly structured JSON formats.
* **Strict Schema Validation:** Utilizes `Pydantic` to ensure extracted data strictly adheres to required formats (e.g., district names, victim counts, emergency statuses).
* **Multi-LLM Routing:** Seamlessly switch between Google Gemini, Groq, and OpenAI models based on task requirements or rate limits.
* **Token Budget Keeper:** Automatically calculates and restricts token limits for incoming messages to manage API costs efficiently.
* **Resilient Processing:** Built-in rate limit handling (Delay mechanisms) to gracefully manage `429 RESOURCE_EXHAUSTED` errors during bulk processing.
* **Automated Reporting:** Exports validated, structured data directly to Pandas DataFrames and Excel reports.

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **Package Manager:** Astral `uv`
* **LLM Integrations:** `google-genai`, `groq`, `openai`
* **Data Validation:** `pydantic`
* **Data Processing:** `pandas`, `openpyxl`
* **Tokenization:** `tiktoken`

## 📂 Project Structure

```text
├── config/                 # Environment configurations and prompt templates
├── data/                   # Raw input data (incidents, news_feed.txt)
├── notebooks/              # Jupyter notebooks for step-by-step execution
├── output/                 # Generated structured reports (e.g., flood_report.xlsx)
├── utils/                  # Core utility modules
│   ├── json_utils.py       # JSON extraction, repair, and schema validation
│   ├── llm_client.py       # Unified LLM API client wrapper
│   ├── router.py           # Model selection and routing logic
│   └── token_utils.py      # Token counting and budget management
├── .env.example            # Example environment variables
└── pyproject.toml          # Project dependencies (managed by uv)