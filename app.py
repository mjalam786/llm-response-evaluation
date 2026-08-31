import streamlit as st
from llm_evaluator import evaluate_response


# Constants
RESPONSE_A = "Response A"
RESPONSE_B = "Response B"
MAX_SCORE = 5
TIE_RESULT = "Tie"


# Page configuration
st.set_page_config(
    page_title="LLM Response Evaluator",
    page_icon="🤖",
    layout="wide"
)


# Application title
st.title("🤖 LLM Response Evaluation System")

st.write(
    "Compare two AI-generated responses using an LLM evaluator."
)

st.divider()


# Question input
question = st.text_area(
    "Question",
    placeholder="Enter the question being answered...",
    height=100
)


# Response inputs
col1, col2 = st.columns(2)


with col1:

    st.subheader(RESPONSE_A)

    response_a = st.text_area(
        f"Enter {RESPONSE_A}",
        placeholder="Paste the first AI response here...",
        height=250,
        key="response_a"
    )


with col2:

    st.subheader(RESPONSE_B)

    response_b = st.text_area(
        f"Enter {RESPONSE_B}",
        placeholder="Paste the second AI response here...",
        height=250,
        key="response_b"
    )


st.divider()


# Evaluation button
if st.button(
    "🚀 Evaluate Responses",
    use_container_width=True
):

    # Validate inputs
    if not question.strip():

        st.warning("Please enter a question.")

    elif not response_a.strip():

        st.warning(f"Please enter {RESPONSE_A}.")

    elif not response_b.strip():

        st.warning(f"Please enter {RESPONSE_B}.")

    else:

        try:

            # Run LLM evaluations
            with st.spinner("Evaluating responses..."):

                evaluation_a = evaluate_response(
                    question,
                    response_a
                )

                evaluation_b = evaluate_response(
                    question,
                    response_b
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
                sum(scores_a) / len(scores_a),
                2
            )

            evaluation_b["overall_score"] = round(
                sum(scores_b) / len(scores_b),
                2
            )


            # Determine winner
            if (
                evaluation_a["overall_score"]
                > evaluation_b["overall_score"]
            ):

                winner = RESPONSE_A

            elif (
                evaluation_b["overall_score"]
                > evaluation_a["overall_score"]
            ):

                winner = RESPONSE_B

            else:

                winner = TIE_RESULT


            # Calculate score difference
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

            # Display results
            st.divider()

            st.header("📊 Evaluation Results")


            # Overall scores
            score_col1, score_col2 = st.columns(2)


            with score_col1:

                st.metric(
                    RESPONSE_A,
                    f"{evaluation_a['overall_score']} / {MAX_SCORE}"
                )


            with score_col2:

                st.metric(
                    RESPONSE_B,
                    f"{evaluation_b['overall_score']} / {MAX_SCORE}"
                )


            # Winner
            if winner == RESPONSE_A:

                st.success(
                    f"🏆 Winner: {RESPONSE_A}"
                )

            elif winner == RESPONSE_B:

                st.success(
                    f"🏆 Winner: {RESPONSE_B}"
                )

            else:

                st.info(
                    "🤝 Result: Tie"
                )


            # Score difference
            st.info(
    f"Score difference: {score_difference} points | "
    f"Confidence: {confidence}"
)


            st.divider()


            # Detailed evaluation
            st.subheader("📋 Detailed Evaluation")


            criteria = [
                "accuracy",
                "relevance",
                "completeness",
                "clarity",
                "instruction_following"
            ]


            # Table headers
            header_col1, header_col2 = st.columns(2)


            with header_col1:

                st.markdown(
                    f"### {RESPONSE_A}"
                )


            with header_col2:

                st.markdown(
                    f"### {RESPONSE_B}"
                )


            # Display each criterion
            for criterion in criteria:

                score_col1, score_col2 = st.columns(2)

                criterion_name = (
                    criterion
                    .replace("_", " ")
                    .title()
                )


                with score_col1:

                    st.write(
                        f"**{criterion_name}:** "
                        f"{evaluation_a[criterion]}/{MAX_SCORE}"
                    )


                with score_col2:

                    st.write(
                        f"**{criterion_name}:** "
                        f"{evaluation_b[criterion]}/{MAX_SCORE}"
                    )


            st.divider()

            # Score comparison chart
            st.subheader("📊 Score Comparison")

            chart_data = {
                "Criterion": [
                    "Accuracy",
                    "Relevance",
                    "Completeness",
                    "Clarity",
                    "Instruction Following"
                ],
                RESPONSE_A: [
                    evaluation_a["accuracy"],
                    evaluation_a["relevance"],
                    evaluation_a["completeness"],
                    evaluation_a["clarity"],
                    evaluation_a["instruction_following"]
                ],
                RESPONSE_B: [
                    evaluation_b["accuracy"],
                    evaluation_b["relevance"],
                    evaluation_b["completeness"],
                    evaluation_b["clarity"],
                    evaluation_b["instruction_following"]
                ]
            }

            st.bar_chart(
                chart_data,
                x="Criterion",
                y=[RESPONSE_A, RESPONSE_B]
            )

            # Reasoning
            st.subheader("🧠 Evaluation Reasoning")

            reasoning_col1, reasoning_col2 = st.columns(2)

            with reasoning_col1:
                st.markdown(
                    f"### {RESPONSE_A}"
                )

                st.write(
                    evaluation_a["reasoning"]
                )

            with reasoning_col2:
                st.markdown(
                    f"### {RESPONSE_B}"
                )

                st.write(
                    evaluation_b["reasoning"]
                )

        except Exception as error:
            st.error(
                "An error occurred while evaluating the responses."
            )

            st.exception(error)

    st.divider()

with st.expander("ℹ️ About This Evaluation"):

    st.write(
        """
        This application uses an LLM as an automated evaluator.
        
        Each response is evaluated independently across five criteria:
        
        • Accuracy
        • Relevance
        • Completeness
        • Clarity
        • Instruction Following
        
        Each criterion receives a score from 1 to 5.
        
        The overall score is calculated as the arithmetic mean
        of the five criterion scores.
        
        The system also generates qualitative reasoning explaining
        the most important strengths or weaknesses of each response.
        
        The winner is determined by comparing the overall scores.
        """
    )        