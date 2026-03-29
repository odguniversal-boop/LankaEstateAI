import streamlit as st
import requests
import json

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LankaEstate AI",
    page_icon="🏡",
    layout="centered"
)

# ─── Your n8n Webhook URL ──────────────────────────────────────────────────────
# Replace this with your actual n8n webhook URL after setting it up
N8N_WEBHOOK_URL = "https://odguniversal.app.n8n.cloud/webhook-test/LankaEstate"

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@300;400;500&display=swap');

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f1923 0%, #1a2d1f 50%, #0f1923 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide default streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 780px; }

    /* Header */
    .lanka-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 2rem;
    }
    .lanka-logo {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        color: #c8a96e;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .lanka-tagline {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.4);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }

    /* Chat messages */
    .msg-user {
        display: flex;
        justify-content: flex-end;
        margin: 1rem 0;
    }
    .msg-user .bubble {
        background: #c8a96e;
        color: #0f1923;
        padding: 0.75rem 1.1rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        font-size: 0.92rem;
        font-weight: 500;
        line-height: 1.5;
    }
    .msg-ai {
        display: flex;
        justify-content: flex-start;
        margin: 1rem 0;
        gap: 0.6rem;
        align-items: flex-start;
    }
    .msg-ai .avatar {
        width: 32px;
        height: 32px;
        background: rgba(200,169,110,0.15);
        border: 1px solid rgba(200,169,110,0.3);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .msg-ai .bubble {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: rgba(255,255,255,0.88);
        padding: 0.75rem 1.1rem;
        border-radius: 4px 18px 18px 18px;
        max-width: 80%;
        font-size: 0.92rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* Welcome card */
    .welcome-card {
        background: rgba(200,169,110,0.06);
        border: 1px solid rgba(200,169,110,0.2);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .welcome-card h3 {
        color: #c8a96e;
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        margin: 0 0 0.5rem 0;
    }
    .welcome-card p {
        color: rgba(255,255,255,0.5);
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.6;
    }

    /* Suggestion chips */
    .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        justify-content: center;
    }
    .chip {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.6);
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.8rem;
        cursor: pointer;
    }

    /* Input area */
    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
        padding: 0.75rem 1rem !important;
    }
    .stTextInput input:focus {
        border-color: rgba(200,169,110,0.5) !important;
        box-shadow: 0 0 0 2px rgba(200,169,110,0.1) !important;
    }
    .stTextInput input::placeholder { color: rgba(255,255,255,0.3) !important; }

    /* Button */
    .stButton button {
        background: #c8a96e !important;
        color: #0f1923 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        font-size: 0.9rem !important;
        transition: all 0.2s !important;
    }
    .stButton button:hover {
        background: #d4b87a !important;
        transform: translateY(-1px) !important;
    }

    /* Clear button */
    .stButton.clear button {
        background: rgba(255,255,255,0.05) !important;
        color: rgba(255,255,255,0.4) !important;
        font-weight: 400 !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 1rem !important;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* Scrollable chat area */
    .chat-container {
        max-height: 480px;
        overflow-y: auto;
        padding-right: 4px;
        margin-bottom: 1rem;
    }

    /* Status bar */
    .status-bar {
        text-align: center;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.2);
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 1rem 0 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lanka-header">
    <div class="lanka-logo">🏡 LankaEstate AI</div>
    <div class="lanka-tagline">Sri Lanka's Conversational Property Finder</div>
</div>
""", unsafe_allow_html=True)


# ─── Welcome card (only if no messages yet) ───────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h3>Welcome! How can I help you today?</h3>
        <p>Tell me what you're looking for — budget, location, number of rooms,<br>
        or any other preference. I'll find the best matches for you.</p>
    </div>
    <div class="chips">
        <span class="chip">🏠 Houses under 30 million</span>
        <span class="chip">📍 Properties near Colombo</span>
        <span class="chip">🌿 Land for sale in Gampaha</span>
        <span class="chip">✅ Bimsaviya properties only</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Chat History ─────────────────────────────────────────────────────────────
chat_html = '<div class="chat-container">'
for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += f'''
        <div class="msg-user">
            <div class="bubble">{msg["content"]}</div>
        </div>'''
    else:
        chat_html += f'''
        <div class="msg-ai">
            <div class="avatar">🏡</div>
            <div class="bubble">{msg["content"]}</div>
        </div>'''
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)


# ─── Input ────────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "message",
            placeholder="e.g. Show me houses under 30 million near Colombo...",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("Send")


# ─── Handle submission ────────────────────────────────────────────────────────
if submitted and user_input.strip():
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Call n8n webhook
    with st.spinner("Finding properties..."):
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "chatInput": user_input,
                    "sessionId": st.session_state.session_id
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                # n8n returns output in different formats — handle both
                if isinstance(data, list):
                    ai_reply = data[0].get("output", data[0].get("text", "Sorry, I could not find a response."))
                elif isinstance(data, dict):
                    ai_reply = data.get("output", data.get("text", data.get("message", "Sorry, I could not find a response.")))
                else:
                    ai_reply = str(data)
            else:
                ai_reply = f"Sorry, something went wrong (Error {response.status_code}). Please try again."

        except requests.exceptions.Timeout:
            ai_reply = "The request timed out. Please try again."
        except Exception as e:
            ai_reply = f"Connection error: {str(e)}"

    # Add AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    st.rerun()


# ─── Clear chat ───────────────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Clear chat", key="clear"):
            st.session_state.messages = []
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()


# ─── Status bar ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-bar">
    Powered by Groq · Built with n8n · LankaEstate AI v1.0
</div>
""", unsafe_allow_html=True)
