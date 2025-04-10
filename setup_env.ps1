# setup_env.ps1

$ErrorActionPreference = "Stop"

Write-Host "📦 Creating virtual environment in .venv..."

python -m venv .venv

$activateScript = ".\.venv\Scripts\Activate.ps1"
if (-Not (Test-Path $activateScript)) {
    Write-Error "❌ Unable to locate the activation script: $activateScript"
}

Write-Host "✅ Virtual environment created."
Write-Host "⏳ Activating virtual environment..."

& $activateScript

Write-Host "✅ Virtual environment activated."
Write-Host "📄 Installing dependencies..."

$requirementsPath = "requirements.txt"
if (Test-Path $requirementsPath) {
    pip install -r $requirementsPath
} else {
    Write-Host "⚠️ requirements.txt file not found. Installing dependencies directly..."
    pip install rouge-score
    pip install sentence-transformers
    pip freeze > requirements.txt
    Write-Host "✅ requirements.txt generated."
}

# Creating directory structure
Write-Host "📁 Creating directory structure and empty files..."
New-Item -ItemType Directory -Path "data/benchmarks" -Force | Out-Null
New-Item -ItemType Directory -Path "data/llm_response" -Force | Out-Null
New-Item -ItemType Directory -Path "data/results" -Force | Out-Null

# Creating empty .json files
"" | Out-File -Encoding utf8 -FilePath "data/benchmarks/benchmark.json"
"" | Out-File -Encoding utf8 -FilePath "data/llm_response/llm_response.json"

# Creating default configuration JSON
$configPath = "params.json"
$configContent = @{
    json_path_benchmark = "data/benchmarks/benchmark.json"
    json_path_responses = "data/llm_response/llm_response.json"
    output_path = "data/results/results.json"
    threshold = 0.75
    semantic_threshold = 0.85
} | ConvertTo-Json -Depth 2

Set-Content -Path $configPath -Value $configContent -Encoding UTF8
Write-Host "📝 Configuration file created at: $configPath"
