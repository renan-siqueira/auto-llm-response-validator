# ✅ Auto LLM Response Validator

Automatically validate LLM-generated answers against a local benchmark. Evaluation via semantic similarity and ROUGE.  
Ready to use with **one command**, no external APIs.

---

## ⚡ Quick Start

### 🪟 Windows (PowerShell)

```powershell
./setup_env.ps1
```

### 🐧 Linux/macOS (bash)

```bash
chmod +x setup_env.sh
./setup_env.sh
```

These setup scripts:

- 🔧 Create a Python virtual environment
- 📦 Install all dependencies
- 📁 Create folder structure and necessary files
- 📝 Generate a default config (`params.json`)

✅ **Everything that can be automated is automated.**  
🧠 The only thing you need to do is populate `benchmark.json` and `llm_response.json` correctly.

---

## 📁 Project Structure

```bash
data/
├── benchmarks/benchmark.json           # Expected answers
├── llm_response/llm_response.json      # LLM-generated answers
└── results/results.json                # Final evaluation report

params.json                             # Configuration and thresholds
models/all-MiniLM-L6-v2/                # Local model (included)
```

---

## 📘 benchmark.json

```json
[
  {
    "id": "1",
    "question": "Your question here!",
    "answer": "Expected answer here!"
  }
]
```

---

## 📙 llm_response.json

Supports **one or multiple answers per question**:

```json
[
  { "id": "1", "question": "Your question here!", "answer": "LLM Model Answer 1" },
  { "id": "1", "question": "Your question here!", "answer": "LLM Model Answer 2" }
]
```

---

## 📊 Output example

```json
{
  "id": "1",
  "question": "...",
  "expected": "...",
  "generated": "...",
  "rouge_score": 0.75,
  "semantic_score": 0.83,
  "passed": false
}
```

Console summary:

```
[✔] 22/30 answers passed (threshold = 0.85)
[ℹ️ ] Accuracy: 73.33%
```

---

## 🚀 Run the Validation

```bash
python validate_response.py [--json-path] [your-path-params.json]
```