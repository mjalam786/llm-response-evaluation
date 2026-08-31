from openai import OpenAI
import json
import os

print("API key loaded:", bool(os.environ.get("OPENROUTER_API_KEY")))
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
    )
def evaluate_response(question, response):

    prompt = f"""
You are an expert evaluator of AI-generated responses.

Evaluate the following response objectively.

QUESTION:
{question}

RESPONSE:
{response}

Evaluate these five criteria from 1 to 5:

1. Accuracy
2. Relevance
3. Completeness
4. Clarity
5. Instruction Following
Did the response follow the explicit instructions and constraints in the question?
If the question contains no special formatting, length, style, or other constraints, give a score of 5 when the response directly attempts to answer the question.
Do not penalize a response for failing to follow instructions that were never given.

Scoring:
5 = Excellent                       
4 = Good
3 = Acceptable / Partially correct
2 = Poor
1 = Very poor

Evaluate each criterion independently.
Identify factual errors when present.
Do not give a high score merely because the response is well written.

Provide a short explanation of the most important strengths or weaknesses.

Return ONLY valid JSON:

{{
    "accuracy": 0,
    "relevance": 0,
    "completeness": 0,
    "clarity": 0,
    "instruction_following": 0,
    "reasoning": "Brief explanation of the evaluation"
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
         response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "evaluation",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "accuracy": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "relevance": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "completeness": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "clarity": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "instruction_following": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "reasoning": {
                        "type": "string"
                    }
                },
                "required": [
                    "accuracy",
                    "relevance",
                    "completeness",
                    "clarity",
                    "instruction_following",
                    "reasoning"
                ],
                "additionalProperties": False
            }
        }
    }

)

    result = response.choices[0].message.content

    print("\nRAW LLM RESPONSE:")
    print(result)

    evaluation = json.loads(result)
    print("\nPARSED EVALUATION:")
    print(evaluation)

    # Make sure reasoning always exists
    if "reasoning" not in evaluation:
        evaluation["reasoning"] = "No reasoning was returned by the model."

    return evaluation