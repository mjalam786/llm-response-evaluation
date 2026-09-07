import json
from statistics import mean


INPUT_FILE = "dataset_results.json"
OUTPUT_FILE = "dataset_analysis.json"

CRITERIA = [
    "accuracy",
    "relevance",
    "completeness",
    "clarity",
    "instruction_following"
]


def get_overall_score(evaluation):
    return mean(
        evaluation[criterion]
        for criterion in CRITERIA
    )


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)

    total = len(results)

    a_scores = []
    b_scores = []
    a_wins = 0
    b_wins = 0
    ties = 0

    criterion_results = {
        criterion: {"response_a": [], "response_b": []}
        for criterion in CRITERIA
    }

    for item in results:
        evaluation_a = item["evaluation_a"]
        evaluation_b = item["evaluation_b"]

        score_a = get_overall_score(evaluation_a)
        score_b = get_overall_score(evaluation_b)

        a_scores.append(score_a)
        b_scores.append(score_b)

        if score_a > score_b:
            a_wins += 1
        elif score_b > score_a:
            b_wins += 1
        else:
            ties += 1

        for criterion in CRITERIA:
            criterion_results[criterion]["response_a"].append(
                evaluation_a[criterion]
            )
            criterion_results[criterion]["response_b"].append(
                evaluation_b[criterion]
            )

    analysis = {
        "total_examples": total,
        "response_a": {
            "average_score": round(mean(a_scores), 2),
            "wins": a_wins
        },
        "response_b": {
            "average_score": round(mean(b_scores), 2),
            "wins": b_wins
        },
        "ties": ties,
        "criterion_averages": {}
    }

    for criterion in CRITERIA:
        analysis["criterion_averages"][criterion] = {
            "response_a": round(
                mean(criterion_results[criterion]["response_a"]), 2
            ),
            "response_b": round(
                mean(criterion_results[criterion]["response_b"]), 2
            )
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=2)

    print("\n===== DATASET ANALYSIS =====")
    print(f"Total examples: {total}")
    print(f"Response A average: {analysis['response_a']['average_score']}")
    print(f"Response B average: {analysis['response_b']['average_score']}")
    print(f"Response A wins: {a_wins}")
    print(f"Response B wins: {b_wins}")
    print(f"Ties: {ties}")

    print("\n===== CRITERION AVERAGES =====")

    for criterion, scores in analysis["criterion_averages"].items():
        print(
            f"{criterion}: "
            f"A={scores['response_a']} | "
            f"B={scores['response_b']}"
        )

    print(f"\nAnalysis saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()