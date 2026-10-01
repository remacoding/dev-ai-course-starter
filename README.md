# Project name

Starter template for the **Development of AI Applications** course final group project.

### Project Idea: AI Data Analysis Assistant

## Team members

- Reng Majer (reng.majer@student.hamk.fi)

## Problem

### Intended users
Who are the primary target users of this application?

- Primary user targets are **freelance data-analysts** and **small-business owners** who work with spreadsheets and datasets that can be analyzed.

### Problem statement
- Freelance data-analysts spend hours on writing complex sql queries or generating excel formulas and reports that can be automated by agentic AI.
- Small-business owners do not have the technical skills to analyse data, Agentic AI can help generate dashboards and reports by the use of natural language such as English. This helps reduce costs and enable the owner to focus on higher-level strategy.

### Why AI is appropriate
- Traditional software limits users to rigid, pre-built queries and standard dashboards. An agentic AI understands natural language, dynamically inspects unknown dataset schemas, generates and safely executes custom SQL/Python code.

## Solution
- The Data Analysis AI Assistant is a specialized, privacy-focused browser AI tool that acts as an automated data co-pilot. Users upload files such as xlsx or csv filetypes, and ask questions in plain English.
- The application inspects the file schema, constructs and safely executes Excel/Pandas/SQL logic, handles syntax errors, and presents key findings along with interactive charts.

## Main user workflow

1. **User Input:** The user uploads a dataset (`.xlsx`, `.csv`, or `.db`) and submits a natural language data question via the Gradio user interface.
2. **Schema Extraction & Guardrails:** The service layer parses file headers and metadata, validates input parameters, and passes schema context to the AI model client.
3. **Model Code Generation:** The ollama model (`qwen3:8b`) generates executable Python/Pandas or SQL code targeted to answer the prompt.
4. **Tool Execution Loop:** The execution engine safely runs the code against the uploaded file, retrieves dataframes or chart objects, and passes execution status back to `ai_service.py`. If an execution error occurs, an error recovery loop feeds the stack trace back to the model for self-correction.
5. **Output Display:** The service layer returns structured text summaries and interactive chart outputs to the Gradio interface.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
1. Extract File Schema (Pandas / SQL)
2. Coordinate Model Prompting
3. Handle Self-Correction Loop
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM Server)
1. Generate executable code
2. Generates Output Dataframe & Matplotlib/Plotly Charts
  ↓
Gradio UI (app/ui.py) [Displays Answer + Rendered Charts]
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model

- **Model used:** `llama3.8` (subject to change depending on hardware performance)

### **Selection rationale:**

* **Data Privacy:** Runs 100% locally via Ollama, preventing confidential client data leaks to third-party APIs.
* **Code Precision:** Outperforms general-purpose models at writing complex, error-free SQL queries and Python/Pandas logic.

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [ ] RAG (Retrieval-Augmented Generation)
- [x] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification

LLMs hallucinate when calculating raw data in text. **Tools / External API integration** allow the model to run real Python/SQL code on datasets, guaranteeing 100% accurate calculations, instant data processing, and reliable chart generation.

## Setup

### 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables

Copy `.env.example` to create your local `.env` configuration file:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Ensure `.env` contains valid values for `OLLAMA_BASE_URL` and `MODEL_NAME`:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.8
```

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama run llama3.8
```

### 5. Run the application

Run the application from the root directory of the project:

```bash
python -m app.main
```

Then open your browser at `http://localhost:7860`.

### 6. Run automated tests

```bash
pytest
```

## Evaluation

1. **Schema Extraction:** Accuracy of column name and type detection across sample `.xlsx` and `.csv` files.
2. **Code Accuracy:** Verification that generated SQL/Pandas code returns correct calculations for standard queries (aggregations, filters, group-bys).
3. **Chart Rendering:** Reliability of generating valid, non-empty plot outputs for requested visualization queries.

Describe your evaluation methodology and summarize key results. Starter test cases can be found in [`evaluation/test_cases.json`](evaluation/test_cases.json).

Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

* **Large File Memory Limits:** Processing datasets over 1000 MB directly in local RAM can cause high latency or out-of-memory crashes depending on system hardware.
* **Messy Excel Formatting:** Files with merged cells, multi-line headers, or missing column names can break automatic schema extraction and cause code execution errors.


## Future improvements

* Interactive Charting: Upgrade static plot images to interactive Plotly charts so users can hover, zoom, and filter data directly inside the UI.
* Auto-Recovery Loop: Add automatic error feedback so the model reads execution stack traces and self-corrects bad code syntax without user intervention.