import json
from llm_evaluator import evaluate_response
# Load the evaluation dataset
with open("prompts.json", "r") as file:
    data = json.load(file)

def calculate_score(scores):
    return sum(scores) / len(scores)


results = []

for item in data:

    # Evaluate Response A using the LLM
    evaluation_a = evaluate_response(
        item["question"],
        item["response_a"]
    )

    # Evaluate Response B using the LLM
    evaluation_b = evaluate_response(
        item["question"],
        item["response_b"]
    )

    # Calculate scores for Response A
    scores_a = [
        evaluation_a["accuracy"],
        evaluation_a["relevance"],
        evaluation_a["completeness"],
        evaluation_a["clarity"],
        evaluation_a["instruction_following"]
    ]

    # Calculate scores for Response B
    scores_b = [
        evaluation_b["accuracy"],
        evaluation_b["relevance"],
        evaluation_b["completeness"],
        evaluation_b["clarity"],
        evaluation_b["instruction_following"]
    ]

    # Calculate overall scores
    evaluation_a["overall_score"] = round(
        calculate_score(scores_a), 2
    )

    evaluation_b["overall_score"] = round(
        calculate_score(scores_b), 2
    )

    # Determine winner
    if evaluation_a["overall_score"] > evaluation_b["overall_score"]:
        winner = "Response A"

    elif evaluation_b["overall_score"] > evaluation_a["overall_score"]:
        winner = "Response B"

    else:
        winner = "Tie"
    score_difference = round(
    abs(
        evaluation_a["overall_score"]
        - evaluation_b["overall_score"]
    ),
    2
)
    if score_difference >= 1.5:
        confidence = "High"
    elif score_difference >= 0.5:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    # Store complete evaluation results
    result = {
    "question": item["question"],
    "response_a": item["response_a"],
    "evaluation_a": evaluation_a,
    "response_b": item["response_b"],
    "evaluation_b": evaluation_b,
    "winner": winner,
    "score_difference": score_difference,
    "confidence": confidence
}

    results.append(result)

a_scores = [
    result["evaluation_a"]["overall_score"]
    for result in results
]

b_scores = [
    result["evaluation_b"]["overall_score"]
    for result in results
]

a_wins = sum(
    1 for result in results
    if result["winner"] == "Response A"
)

b_wins = sum(
    1 for result in results
    if result["winner"] == "Response B"
)

ties = sum(
    1 for result in results
    if result["winner"] == "Tie"
)

average_a = round(sum(a_scores) / len(a_scores), 2)
average_b = round(sum(b_scores) / len(b_scores), 2)

print("\n" + "=" * 40)
print("LLM EVALUATION SUMMARY")
print("=" * 40)

print(f"Questions evaluated: {len(results)}")
print(f"Response A wins: {a_wins}")
print(f"Response B wins: {b_wins}")
print(f"Ties: {ties}")

print(f"Average Response A score: {average_a}")
print(f"Average Response B score: {average_b}")

if average_a > average_b:
    print("Overall winner: Response A")
elif average_b > average_a:
    print("Overall winner: Response B")
else:
    print("Overall winner: Tie")

print("=" * 40)
# Save results
with open("results.json", "w") as file:
    json.dump(results, file, indent=4)


print("\nEvaluation completed!")
print("Results saved to results.json")