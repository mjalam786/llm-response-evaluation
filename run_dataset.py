import json
from llm_evaluator import evaluate_response


INPUT_FILE = "evaluation_dataset.json"
OUTPUT_FILE = "dataset_results.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    results = []

    for item in dataset:
        print(f"Evaluating {item['id']}/30...")

        evaluation_a = evaluate_response(
            item["question"],
            item["response_a"]
        )

        evaluation_b = evaluate_response(
            item["question"],
            item["response_b"]
        )

        results.append({
            "id": item["id"],
            "question": item["question"],
            "response_a": item["response_a"],
            "response_b": item["response_b"],
            "evaluation_a": evaluation_a,
            "evaluation_b": evaluation_b
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("\nEvaluation complete!")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()