import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Health Assistant")
st.caption("General health & wellness information — not a substitute for professional medical advice.")

with st.sidebar:
    st.header("Student Details")
    name = st.text_input("Name", placeholder="Enter your name")
    reg_no = st.text_input("Registration Number", placeholder="Enter registration number")

    st.divider()
    st.subheader("Try these questions")
    examples = [
        "Why is sleep important?",
        "What is BMI?",
        "Why should we drink enough water?",
        "What are the benefits of exercise?"
    ]
    for q in examples:
        st.write("• " + q)

    st.divider()
    st.info("For emergencies or serious symptoms, contact a qualified healthcare professional or local emergency service.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a general health or wellness question...")

if question:
    if not name or not reg_no:
        st.warning("Please enter your Name and Registration Number in the sidebar first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    system_prompt = """You are an AI Health Assistant for a student educational project.
Answer general health and wellness questions in simple, clear language.
You may explain topics such as sleep, hydration, nutrition, exercise, BMI, stress management,
and healthy lifestyle habits.

Safety rules:
- Do not diagnose diseases or claim certainty about a user's condition.
- Do not prescribe medicines, dosages, or personalized treatment.
- For symptoms that could be serious, advise the user to consult a qualified healthcare professional.
- For emergencies, advise contacting local emergency services immediately.
- Keep answers educational and concise, preferably using short headings or bullet points.
- Clearly distinguish general information from individualized medical advice.
"""

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=system_prompt,
            input=question
        )
        answer = response.output_text
    except Exception as e:
        answer = (
            "I couldn't connect to the AI service. Please check that your "
            "`OPENAI_API_KEY` is configured correctly in Streamlit Secrets.\n\n"
            f"Technical detail: `{e}`"
        )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
st.caption("Educational project • AI Health Assistant")
