import os
import json
import argparse

from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util


# Local utils
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Metrics
def compute_rouge_score(expected, generated):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(expected, generated)
    return score['rougeL'].fmeasure


def compute_semantic_score(model, expected, generated):
    embeddings = model.encode([expected, generated], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return float(score)


def compare_responses(benchmark, generated, semantic_threshold=0.85):
    results = []
    total, passed = 0, 0

    model = SentenceTransformer('models/all-MiniLM-L6-v2')

    # Group all generated answers by ID
    generated_grouped = {}
    for item in generated:
        generated_grouped.setdefault(item["id"], []).append(item)

    for benchmark_entry in benchmark:
        entry_id = benchmark_entry["id"]
        expected = benchmark_entry.get("answer", "").strip()

        if not expected or entry_id not in generated_grouped:
            continue

        for answer_entry in generated_grouped[entry_id]:
            answer = answer_entry.get("answer", "").strip()
            if not answer:
                continue

            rouge_score = compute_rouge_score(expected, answer)
            semantic_score = compute_semantic_score(model, expected, answer)
            success = semantic_score >= semantic_threshold

            results.append({
                "id": entry_id,
                "question": benchmark_entry.get("question", ""),
                "expected": expected,
                "generated": answer,
                "rouge_score": round(rouge_score, 4),
                "semantic_score": round(semantic_score, 4),
                "passed": success,
                "expected_score": semantic_threshold
            })

            total += 1
            if success:
                passed += 1

    summary = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "accuracy": round(passed / total * 100, 2),
        "semantic_threshold": semantic_threshold
    }

    return results, summary


def print_summary(summary, results=None, top_n=5):
    print(f"\n\n[✔] {summary['passed']}/{summary['total']} answers passed (threshold = {summary['semantic_threshold']})")
    print(f"[ℹ️ ] Accuracy: {summary['accuracy']}%\n")

    if results:
        print(f"🔎 Top {top_n} answers with lowest similarity:")
        # Sort by lowest semantic score
        sorted_results = sorted(results, key=lambda r: r["semantic_score"])
        for r in sorted_results[:top_n]:
            status = "✅" if r["passed"] else "❌"
            print(f"  {status} ID {r['id']} - Score: {r['semantic_score']} | Question: {r['question']}")



def save_report(results, output_path='comparison_result.json'):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[💾] Report saved to: {output_path}\n\n")


def validate_llm_responses(params):
    benchmark_path = params["json_path_benchmark"]
    responses_path = params["json_path_responses"]
    output_path = params.get("output_path", "comparison_result.json")
    semantic_threshold = params.get("semantic_threshold", 0.85)

    if not os.path.exists(benchmark_path):
        raise FileNotFoundError(f"Benchmark file not found: {benchmark_path}")
    if not os.path.exists(responses_path):
        raise FileNotFoundError(f"Responses file not found: {responses_path}")

    benchmark_data = load_json(benchmark_path)
    generated_data = load_json(responses_path)

    results, summary = compare_responses(
        benchmark=benchmark_data,
        generated=generated_data,
        semantic_threshold=semantic_threshold
    )
    print_summary(summary, results=results)
    save_report(results, output_path=output_path)


def main(params_path):
    params = load_json(params_path)
    validate_llm_responses(params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatic validation of LLM responses.")
    parser.add_argument(
        '--json-path',
        type=str,
        default="./params.json",
        help='Path to JSON configuration file'
    )
    args = parser.parse_args()
    main(args.json_path)
