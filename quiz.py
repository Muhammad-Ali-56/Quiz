import streamlit as st
import json

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Quiz", layout="centered",page_icon="📚")
st.title("📚 Quiz")

NEGATIVE_IMPACT = 0.25

# ---------------- LOAD QUESTIONS ----------------
with open("quiz_question.json", "r") as f:
    questions = json.load(f)

TOTAL_QUESTIONS = len(questions)

# ---------------- SESSION STATE INIT ----------------
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = ["E"] * TOTAL_QUESTIONS

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "none"  # options: "none", "user", "correct", "both"

# ---------------- FUNCTIONS ----------------
def restart_test():
    st.session_state.current_index = 0
    st.session_state.user_answers = ["E"] * TOTAL_QUESTIONS
    st.session_state.quiz_finished = False
    st.session_state.view_mode = "none"
    st.rerun()


def calculate_results():
    score = 0
    negative = 0
    correct = 0
    wrong = 0
    not_answered = 0

    for i, q in enumerate(questions):
        ans = st.session_state.user_answers[i]
        if ans == q["correct_answer"]:
            score += 1
            correct += 1
        elif ans == "E":
            not_answered += 1
        else:
            wrong += 1
            negative += NEGATIVE_IMPACT

    return score - negative, correct, wrong, not_answered, negative


# ---------------- QUIZ VIEW ----------------
if not st.session_state.quiz_finished:

    q_index = st.session_state.current_index
    q = questions[q_index]

    st.subheader(f"Question {q_index + 1} of {TOTAL_QUESTIONS}")
    st.write(q["question"])

    option_letters = ["A", "B", "C", "D", "E"]
    option_texts = q["options"].copy()

    if "E. No Response" not in option_texts:
        option_texts.append("E. No Response")

    options = dict(zip(option_letters, option_texts))

    selected = st.radio(
        "Select your answer:",
        options=list(options.keys()),
        format_func=lambda x: options[x],
        index=option_letters.index(st.session_state.user_answers[q_index]),
        key=f"q_{q_index}"
    )

    st.session_state.user_answers[q_index] = selected
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⬅ Back", key="back_btn") and q_index > 0:
            st.session_state.current_index -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡", key="next_btn") and q_index < TOTAL_QUESTIONS - 1:
            st.session_state.current_index += 1
            st.rerun()

    with col3:
        if st.button("✅ Finish Test", key="finish_btn"):
            st.session_state.quiz_finished = True
            st.rerun()

    with col4:
        if st.button("🔄 Restart", key="restart_btn"):
            restart_test()


# ---------------- RESULT VIEW ----------------
else:
    final_score, correct, wrong, not_answered, negative = calculate_results()

    st.success("🎉 Test Completed")

    st.write(f"**Final Score:** {final_score} / {TOTAL_QUESTIONS}")
    st.write(f"Correct Answers: {correct}")
    st.write(f"Wrong Answers: {wrong}")
    st.write(f"Not Answered: {not_answered}")
    st.write(f"Deducted Marks: {negative}")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🧾 Your Answers", key="user_btn"):
            st.session_state.view_mode = "user"

    with col2:
        if st.button("✅ Correct Answers", key="correct_btn"):
            st.session_state.view_mode = "correct"

    with col3:
        if st.button("📊 Both", key="both_btn"):
            st.session_state.view_mode = "both"

    with col4:
        if st.button("🔄 Restart Test", key="restart_result_btn"):
            restart_test()

    # Render answers based on view_mode
    if st.session_state.view_mode in ["user", "both"]:
        st.subheader("🧾 Your Answers")
        for i, ans in enumerate(st.session_state.user_answers):
            st.write(f"Q{i+1}: {ans}")

    if st.session_state.view_mode in ["correct", "both"]:
        st.subheader("✅ Correct Answers")
        for i, q in enumerate(questions):
            st.write(f"Q{i+1}: {q['correct_answer']}")
