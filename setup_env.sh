#!/bin/bash

set -e

echo "📦 Creating virtual environment in .venv..."

python3 -m venv .venv

activate_script="./.venv/bin/activate"
if [ ! -f "$activate_script" ]; then
    echo "❌ Unable to locate the activation script: $activate_script"
    exit 1
fi

echo "✅ Virtual environment created."
echo "⏳ Activating virtual environment..."

# shellcheck disable=SC1090
source "$activate_script"

echo "✅ Virtual environment activated."
echo "📄 Installing dependencies..."

requirements_path="requirements.txt"
if [ -f "$requirements_path" ]; then
    pip install -r "$requirements_path"
else
    echo "⚠️ requirements.txt file not found. Installing dependencies directly..."
    pip install rouge-score
    pip install sentence-transformers
    pip freeze > requirements.txt
    echo "✅ requirements.txt generated."
fi

# Creating directory structure
echo "📁 Creating directory structure and empty files..."
mkdir -p data/benchmarks
mkdir -p data/llm_response
mkdir -p data/results

# Creating empty .json files
: > data/benchmarks/benchmark.json
: > data/llm_response/llm_response.json

# Creating default configuration JSON
config_path="params.json"
cat <<EOF > "$config_path"
{
    "json_path_benchmark": "data/benchmarks/benchmark.json",
    "json_path_responses": "data/llm_response/llm_response.json",
    "output_path": "data/results/results.json",
    "semantic_threshold": 0.85
}
EOF

echo "📝 Configuration file created at: $config_path"
