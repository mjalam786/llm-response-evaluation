# LLM Response Evaluation System

A Python-based framework for evaluating and comparing AI-generated responses using an LLM evaluator.

## Project Overview

This project evaluates AI-generated responses across multiple quality dimensions and compares the results between two candidate responses.

The system uses an LLM to evaluate:

- Accuracy
- Relevance
- Completeness
- Clarity
- Instruction Following

It also generates qualitative reasoning for each evaluation.

## Architecture

Question + Response
        |
        v
LLM Evaluator
        |
        +--> Accuracy
        +--> Relevance
        +--> Completeness
        +--> Clarity
        +--> Instruction Following
        +--> Reasoning
        |
        v
Python Scoring
        |
        v
Overall Score
        |
        v
Response A vs Response B
        |
        v
Winner
        |
        v
results.json

## Human vs LLM Evaluation

The project also compares LLM-generated evaluations against human judgments.

The comparison measures:

- Exact score agreement
- Average score difference
- Per-criterion agreement
- Winner agreement

This helps evaluate the reliability of the LLM evaluator itself.

## Technologies

- Python
- JSON
- OpenRouter API
- OpenAI Python SDK
- Prompt Engineering
- LLM Evaluation

## Evaluation Criteria

Each response receives a score from 1 to 5.

| Score | Meaning |
|---|---|
| 5 | Excellent |
| 4 | Good |
| 3 | Acceptable / Partially Correct |
| 2 | Poor |
| 1 | Very Poor |

## Project Structure

```text
llm-response-evaluation/
│
├── evaluation.py
├── llm_evaluator.py
├── compare_evaluations.py
├── test_llm.py
├── test_openrouter.py
│
├── prompts.json
├── human_scores.json
├── results.json
├── evaluation_summary.json
│
├── .gitignore
└── README.md