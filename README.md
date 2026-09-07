# LLM Response Evaluation System

An AI-powered system for evaluating and comparing LLM-generated responses.

## 🚀 Live Demo

[Try the Live Streamlit App](https://llm-response-evaluation-j493uvrho8mtapg2d3c3my.streamlit.app)

## 📌 Project Overview

This project evaluates AI-generated responses across multiple quality dimensions and compares the results between two candidate responses.

The system uses an LLM to evaluate:

- Accuracy
- Relevance
- Completeness
- Clarity
- Instruction Following

It also generates qualitative reasoning for each evaluation.

## 🏗️ Architecture

```text
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
Evaluation Results