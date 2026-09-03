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


## Evaluation Experiment

The system was evaluated on a dataset of 30 question/response pairs.
Each response was independently evaluated by an LLM across five criteria:

- Accuracy
- Relevance
- Completeness
- Clarity
- Instruction Following

### Results

| Metric | Response A | Response B |
|---|---:|---:|
| Overall Average | 4.69/5 | 2.14/5 |
| Accuracy | 5.00 | 1.00 |
| Relevance | 5.00 | 1.70 |
| Completeness | 3.43 | 1.10 |
| Clarity | 5.00 | 2.67 |
| Instruction Following | 5.00 | 4.23 |
| Wins | 30 | 0 |

### Findings

Response A was preferred in all 30 evaluation examples.

The results also demonstrate why multi-dimensional evaluation is useful. 
Response B received relatively strong instruction-following scores despite 
performing poorly on factual accuracy, showing that following instructions 
does not necessarily mean that a response is correct or useful.

### Limitations

This experiment uses a relatively small dataset and synthetic response pairs.
The results should not be interpreted as proof that the LLM evaluator is 
always reliable. Human evaluation and a larger, more diverse benchmark would 
be required to measure evaluator reliability more rigorously.

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