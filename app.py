````python
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
.hero {
    padding: 1.5rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #e8f5e9, #e3f2fd);
    margin-bottom: 1.5rem;
}
.hero h1 {
    margin-bottom: 0.3rem;
}
.hero p {
    margin-bottom: 0;
    color: #455a64;
}
.disclaimer {
    padding: 0.9rem 1rem;
    border-radius: 12px;
    background-color: #fff8e1;
    border-left: 4px solid #ffb300;
    font-size: 0.9rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.friend-mode {
    padding: 1rem;
    border-radius: 14px;
    background-color: #f3e5f5;
    border-left: 4px solid #8e24aa;
    margin-bottom: 1rem;
}
.section-title {
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}
div.stButton > button {
    border-radius: 10px;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

MODEL_NAME = "gemini-2.5-flash"

@st.cache_resource
def get_gemini_client():
    if "GEMINI_API_KEY" not in st.secrets:
        return None
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

HEALTH_INSTRUCTION = """
You are an AI Health Assistant designed for general health and wellness education.

Provide clear, simple and useful information about sleep, hydration, nutrition,
exercise, BMI, stress, healthy habits and lifestyle.

You are not a doctor and must not present yourself as one.
Do not diagnose diseases or medical conditions.
Do not prescribe medicines or personalized medication dosages.
Do not tell users to start or stop prescription medication.
Do not provide definitive diagnoses based on symptoms.
For serious, severe, persistent or worsening symptoms, recommend consulting
a qualified healthcare professional.
For emergencies, recommend contacting local emergency services immediately.
Do not unnecessarily frighten the user.
Use simple language suitable for students and the general public.
Keep answers concise but useful.
"""

FRIEND_INSTRUCTION = """
You are Friend Mode, a warm, supportive AI companion focused on mental
wellness and everyday emotional support.

Be kind, calm, non-judgmental, friendly, encouraging and respectful.

Listen carefully to what the user says.
Acknowledge their feelings without judging them.
Encourage healthy coping strategies.
You may suggest breathing exercises, walking, journaling, talking to a trusted
person, taking a break, getting enough sleep, or doing something relaxing.
Ask gentle follow-up questions when useful.

Do not pretend to be human or a therapist.
Do not claim to know exactly how the user feels.
Do not diagnose mental health conditions.
Do not prescribe medication.
Do not provide dangerous or harmful instructions.

If the user says they are in immediate danger, intend to hurt themselves,
intend to hurt someone else, or describes an imminent life-threatening
situation, respond seriously and encourage them to contact local emergency
services and a trusted person immediately.

For possible self-harm or suicide concerns, encourage immediate contact with
emergency services or an appropriate crisis service available in their country.
Encourage them to move toward a trusted person and avoid being alone if they
are in immediate danger.

Friend Mode provides emotional support and is not a replacement for
professional mental healthcare.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "friend_mode" not in st.session_state:
    st.session_state.friend_mode = False

with st.sidebar:
    st.title("🩺 Health Assistant")
    st.markdown("### Choose a mode")

    normal_mode = st.button(
        "🩺 Health & Wellness",
        use_container_width=True
    )

    friend_mode_button = st.button(
        "💜 Friend Mode",
        use_container_width=True
    )

    if normal_mode:
        st.session_state.friend_mode = False
        st.session_state.messages = []
        st.rerun()

    if friend_mode_button:
        st.session_state.friend_mode = True
        st.session_state.messages = []
        st.rerun()

    st.divider()

    if st.session_state.friend_mode:
        st.markdown("### 💜 Friend Mode")
        st.write(
            "A supportive space for everyday feelings, stress, "
            "motivation and mental wellness."
        )
    else:
        st.markdown("### 🩺 Health Mode")
        st.write(
            "Ask general questions about health, fitness, nutrition "
            "and healthy lifestyle habits."
        )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Educational project powered by Google Gemini.")

if st.session_state.friend_mode:
    st.markdown("""
    <div class="hero">
        <h1>💜 Friend Mode</h1>
        <p>
            A calm, supportive space to talk about your day,
            stress, motivation and everyday feelings.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="friend-mode">
        <b>You're welcome here.</b><br>
        You can talk about what's bothering you, ask for motivation,
        or simply have a conversation.
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="hero">
        <h1>🩺 AI Health Assistant</h1>
        <p>
            Ask questions about health, wellness, fitness,
            nutrition and healthy lifestyle habits.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Important:</b> This assistant provides general educational
    information and is not a substitute for professional medical advice.
    For serious or emergency symptoms, contact a qualified healthcare
    professional or local emergency service.
</div>
""", unsafe_allow_html=True)

if not st.session_state.friend_mode:
    st.markdown(
        '<h3 class="section-title">💡 Quick Questions</h3>',
        unsafe_allow_html=True
    )

    st.caption("Click a question to get an answer instantly.")

    quick_questions = [
        "Why is sleep important?",
        "What is BMI?",
        "Why should we drink enough water?",
        "What are the benefits of exercise?",
        "How many hours of sleep do adults need?",
        "What is a balanced diet?",
        "How can I reduce daily stress?",
        "Why is breakfast important?"
    ]

    cols = st.columns(2)
    selected_question = None

    for index, question in enumerate(quick_questions):
        with cols[index % 2]:
            if st.button(
                question,
                key=f"quick_{index}",
                use_container_width=True
            ):
                selected_question = question

else:
    st.markdown(
        '<h3 class="section-title">💬 You can start with...</h3>',
        unsafe_allow_html=True
    )

    friend_questions = [
        "I'm feeling stressed today.",
        "I don't feel very motivated.",
        "I had a difficult day.",
        "How can I relax when my mind feels busy?",
        "Can you give me some encouragement?",
        "I just want someone to talk to."
    ]

    cols = st.columns(2)
    selected_question = None

    for index, question in enumerate(friend_questions):
        with cols[index % 2]:
            if st.button(
                question,
                key=f"friend_{index}",
                use_container_width=True
            ):
                selected_question = question

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

typed_question = st.chat_input(
    "Talk to me about your health and wellness..."
    if not st.session_state.friend_mode
    else "Tell me what's on your mind..."
)

question = typed_question or selected_question

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    client = get_gemini_client()

    if client is None:
        with st.chat_message("assistant"):
            st.error("Gemini API key is not configured.")
            st.info(
                "Add the following to Streamlit Secrets:\n\n"
                "```toml\n"
                'GEMINI_API_KEY = "your_api_key_here"\n'
                "```"
            )
    else:
        system_instruction = (
            FRIEND_INSTRUCTION
            if st.session_state.friend_mode
            else HEALTH_INSTRUCTION
        )

        conversation = []

        for message in st.session_state.messages:
            role = "user" if message["role"] == "user" else "model"

            conversation.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part(text=message["content"])
                    ]
                )
            )

        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=conversation,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                            max_output_tokens=800
                        )
                    )

                    answer = response.text

                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            with st.chat_message("assistant"):
                st.error(
                    "I'm unable to connect to Gemini right now. "
                    "Please check your API key and try again."
                )

                with st.expander("Technical details"):
                    st.code(str(e))

st.divider()

if st.session_state.friend_mode:
    st.caption(
        "💜 Friend Mode provides supportive conversation, "
        "but it is not a replacement for a mental health professional."
    )
else:
    st.caption(
        "🩺 AI Health Assistant • General educational information only"
    )
````
