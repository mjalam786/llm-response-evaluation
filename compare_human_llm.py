import json
from statistics import mean


LLM_FILE = "dataset_results.json"
HUMAN_FILE = "human_scores.json"

CRITERIA = [
    "accuracy",
    "relevance",
    "completeness",
    "clarity",
    "instruction_following"
]


def overall_score(scores):
    return mean(scores[c] for c in CRITERIA)


def main():
    with open(LLM_FILE, "r", encoding="utf-8") as file:
        llm_results = json.load(file)

    with open(HUMAN_FILE, "r", encoding="utf-8") as file:
        human_results = json.load(file)

    llm_by_question = {
        item["question"]: item
        for item in llm_results
    }

    comparisons = []

    for human in human_results:
        question = human["question"]

        if question not in llm_by_question:
            print(f"Skipping unmatched question: {question}")
            continue

        llm = llm_by_question[question]

        for response_name in ["response_a", "response_b"]:

            llm_scores = llm[
                f"evaluation_{response_name[-1].lower()}"
            ]

            human_scores = human[response_name]

            comparisons.append({
                "question": question,
                "response": response_name,
                "llm_score": round(
                    overall_score(llm_scores), 2
                ),
                "human_score": round(
                    overall_score(human_scores), 2
                )
            })

    differences = [
        abs(item["llm_score"] - item["human_score"])
        for item in comparisons
    ]

    exact_matches = sum(
        item["llm_score"] == item["human_score"]
        for item in comparisons
    )

    agreement_percentage = (
        exact_matches / len(comparisons) * 100
        if comparisons else 0
    )

    average_difference = (
        mean(differences)
        if differences else 0
    )

    output = {
        "matched_questions": len(comparisons) // 2,
        "responses_compared": len(comparisons),
        "exact_score_matches": exact_matches,
        "agreement_percentage": round(
            agreement_percentage, 2
        ),
        "average_absolute_score_difference": round(
            average_difference, 2
        ),
        "comparisons": comparisons
    }

    with open(
        "human_llm_comparison.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(output, file, indent=2)

    print("\n===== HUMAN vs LLM AGREEMENT =====")
    print(
        f"Matched questions: "
        f"{len(comparisons) // 2}"
    )
    print(
        f"Responses compared: "
        f"{len(comparisons)}"
    )
    print(
        f"Exact score agreement: "
        f"{exact_matches}/{len(comparisons)}"
    )
    print(
        f"Agreement: "
        f"{agreement_percentage:.2f}%"
    )
    print(
        f"Average score difference: "
        f"{average_difference:.2f}"
    )

    print("\n===== COMPARISON =====")

    for item in comparisons:
        print(
            f"{item['question']} | "
            f"{item['response']} | "
            f"Human={item['human_score']} | "
            f"LLM={item['llm_score']}"
        )

    print(
        "\nResults saved to "
        "human_llm_comparison.json"
    )


if __name__ == "__main__":
    main()