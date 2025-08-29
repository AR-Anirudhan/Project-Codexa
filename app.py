import streamlit as st
from tutor_engine import get_tutor_response
import re
import time

# --- Page Configuration ---
st.set_page_config(page_title="Project Codexa", page_icon="🧑‍🏫", layout="centered", initial_sidebar_state="expanded")

# --- Helper function to parse the quiz ---
def parse_quiz(text):
    quiz_match = re.search(r"\[QUIZ START\](.*?)\[QUIZ END\]", text, re.DOTALL)
    if not quiz_match: return None, text
    
    quiz_block = quiz_match.group(1).strip()
    text_without_quiz = text.replace(quiz_match.group(0), "\n\nI've prepared a quick question for you!").strip()
    
    code_match = re.search(r"\[CODE\](.*?)\[/CODE\]", quiz_block, re.DOTALL)
    code_snippet = ""
    if code_match:
        code_snippet = code_match.group(1).strip()
        quiz_block = quiz_block.replace(code_match.group(0), "").strip()
        
    question_match = re.search(r"Question: (.*?)\n", quiz_block)
    options_match = re.findall(r"\[([A-C])\] (.*?)\n", quiz_block)
    correct_match = re.search(r"\[CORRECT: ([A-C])\]", quiz_block)
    
    if not question_match or not options_match or not correct_match: return None, text

    quiz_data = {
        "question": question_match.group(1),
        "code": code_snippet,
        "options": {opt[0]: opt[1] for opt in options_match},
        "correct": correct_match.group(1),
        "topic": st.session_state.get("last_topic", "the last topic"),
        "answered": False,
        "user_answer": None
    }
    return quiz_data, text_without_quiz

# --- Session State Initialization ---
if "messages" not in st.session_state: st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("📚 Project Codexa")
    st.write("Your personal AI tutor for a wide range of subjects.")
    st.divider()

    st.subheader("📝 Quick Quiz")
    def quiz_button_callback(topic):
        st.session_state.prompt = f"Generate a medium-difficulty quiz question about {topic}."

    st.button("Math Quiz", on_click=quiz_button_callback, args=["Math"], use_container_width=True)
    st.button("Physics Quiz", on_click=quiz_button_callback, args=["Physics"], use_container_width=True)
    st.button("Python Quiz", on_click=quiz_button_callback, args=["Python programming"], use_container_width=True)
    st.button("English Quiz", on_click=quiz_button_callback, args=["English grammar"], use_container_width=True)
    st.button("Biology Quiz", on_click=quiz_button_callback, args=["Biology"], use_container_width=True)
    st.button("C programming Quiz", on_click=quiz_button_callback, args=["C programming"], use_container_width=True)

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main App Interface ---
st.title("🧑‍🏫 Project Codexa")
st.caption("Unlock your future, in your language.")

# --- Render Chat History and Quizzes ---
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"): st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🧑‍🏫"):
            st.markdown(message["content"])
            if "quiz" in message and message["quiz"]:
                quiz = message["quiz"]
                with st.container(border=True):
                    if quiz["answered"]:
                        if quiz["code"]: st.code(quiz["code"], language='python')
                        st.write(quiz["question"])
                        for key, value in quiz["options"].items():
                            label = f"{key}: {value}"
                            if key == quiz["correct"]: st.success(f"{label} (Correct Answer)")
                            elif key == quiz["user_answer"]: st.error(f"{label} (Your Answer)")
                            else: st.write(label)
                    else:
                        with st.form(key=f"quiz_form_{i}"):
                            if quiz["code"]: st.code(quiz["code"], language='python')
                            st.write(quiz["question"])
                            user_answer = st.radio("Select your answer:", options=list(quiz["options"].keys()), format_func=lambda key: f"{key}: {quiz['options'][key]}", index=None)
                            submitted = st.form_submit_button("Submit Answer")

                            if submitted:
                                if user_answer:
                                    quiz["answered"] = True
                                    quiz["user_answer"] = user_answer
                                    if user_answer == quiz["correct"]:
                                        st.success("Correct! Well done! 🎉")
                                        st.balloons()
                                        compliment_prompt = f"The student answered correctly. Give them a short, encouraging compliment."
                                        compliment_response = get_tutor_response(compliment_prompt, [])
                                        st.session_state.messages.append({"role": "assistant", "content": compliment_response})
                                    else:
                                        st.error(f"Not quite! The correct answer was {quiz['correct']}.")
                                        explanation_prompt = f"The student answered incorrectly. Explain why {quiz['correct']} is the right answer to: {quiz['question']}"
                                        explanation_response = get_tutor_response(explanation_prompt, [])
                                        st.session_state.messages.append({"role": "assistant", "content": explanation_response})
                                    st.rerun()
                                else:
                                    st.warning("Please choose an option.")

# --- Determine if any quiz is currently active ---
is_quiz_active = any("quiz" in msg and msg.get("quiz") and not msg["quiz"]["answered"] for msg in st.session_state.messages)

# --- Welcome Screen & Example Prompts ---
if not st.session_state.messages:
    st.info("Ask me a question to get started, or try one of these examples!")
    col1, col2 = st.columns(2)
    def example_question_callback(question):
        st.session_state.prompt = question
    
    with col1:
        st.button("Explain 'for loops' in Python", on_click=example_question_callback, args=["Explain Python 'for loops'."], use_container_width=True)
        st.button("Explain pointers in C", on_click=example_question_callback, args=["What are pointers in C programming?"], use_container_width=True)
    with col2:
        st.button("Difference between 'see' and 'look'", on_click=example_question_callback, args=["What is the difference between 'see' and 'look'?"], use_container_width=True)
        st.button("What are fractions in Math?", on_click=example_question_callback, args=["Explain what fractions are in Math."], use_container_width=True)


# --- User Input Handling ---
if prompt := st.chat_input("Ask a topic...", disabled=is_quiz_active, key="chat_input") or st.session_state.get("prompt"):
    
    if "prompt" in st.session_state:
        del st.session_state["prompt"]

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.last_topic = prompt
    
    with st.chat_message("assistant", avatar="🧑‍🏫"):
        with st.spinner(""):
            st.image("assets/thinking.gif", width=100)
            ai_response_full = get_tutor_response(prompt, st.session_state.messages)

    quiz_data, ai_response_text = parse_quiz(ai_response_full)
    st.session_state.messages.append({"role": "assistant", "content": ai_response_text, "quiz": quiz_data})
    
    st.rerun()