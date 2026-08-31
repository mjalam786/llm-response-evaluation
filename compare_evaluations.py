import json


# Load LLM evaluation results
with open("results.json", "r") as file:
    llm_results = json.load(file)


# Load human evaluation results
with open("human_scores.json", "r") as file:
    human_results = json.load(file)


criteria = [
    "accuracy",
    "relevance",
    "completeness",
    "clarity",
    "instruction_following"
]


total_comparisons = 0
matching_scores = 0
total_difference = 0

criterion_matches = {
    "accuracy": 0,
    "relevance": 0,
    "completeness": 0,
    "clarity": 0,
    "instruction_following": 0
}

criterion_totals = {
    "accuracy": 0,
    "relevance": 0,
    "completeness": 0,
    "clarity": 0,
    "instruction_following": 0
}


for llm_item, human_item in zip(llm_results, human_results):

    print("\nQuestion:")
    print(llm_item["question"])

    for response_type in ["a", "b"]:

        llm_evaluation = llm_item[f"evaluation_{response_type}"]
        human_evaluation = human_item[f"response_{response_type}"]

        print(f"\nResponse {response_type.upper()}")

        for criterion in criteria:

            llm_score = llm_evaluation[criterion]
            human_score = human_evaluation[criterion]

            difference = abs(llm_score - human_score)

            total_comparisons += 1
            total_difference += difference

            if llm_score == human_score:
                matching_scores += 1

            criterion_totals[criterion] += 1

            if llm_score == human_score:
                criterion_matches[criterion] += 1
                  

            print(
                f"{criterion}: "
                f"Human={human_score}, "
                f"LLM={llm_score}, "
                f"Difference={difference}"
            )


agreement_rate = (
    matching_scores / total_comparisons
) * 100

average_difference = (
    total_difference / total_comparisons
)
criterion_agreement = {}

for criterion in criteria:
    agreement = (
        criterion_matches[criterion]
        / criterion_totals[criterion]
    ) * 100

    criterion_agreement[criterion] = round(
        agreement, 2
    )


print("\n" + "=" * 50)
print("HUMAN vs LLM EVALUATION")
print("=" * 50)

print(f"Total comparisons: {total_comparisons}")
print(f"Exact score matches: {matching_scores}")
print(f"Agreement rate: {agreement_rate:.2f}%")
print(f"Average score difference: {average_difference:.2f}")

print("=" * 50)
summary = {
    "total_comparisons": total_comparisons,
    "exact_score_matches": matching_scores,
    "agreement_rate": round(agreement_rate, 2),
    "average_score_difference": round(average_difference, 2),
    "criterion_agreement": criterion_agreement
}

with open("evaluation_summary.json", "w") as file:
    json.dump(summary, file, indent=4)

print("\nSummary saved to evaluation_summary.json")