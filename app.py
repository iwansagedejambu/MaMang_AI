import streamlit as st
import requests

# --- Konfigurasi halaman
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot via AgentRouter")

# --- Input API Token
if "agent_token" not in st.session_state:
    st.session_state.agent_token = ""

st.session_state.agent_token = st.text_input(
    "Masukkan AgentRouter API Token:",
    type="password",
    value=st.session_state.agent_token
)

AGENT_API_URL = "https://agentrouter.org/v1/chat/completions"

def ask_agentrouter(prompt: str, token: str) -> str:
    """Kirim pertanyaan ke AgentRouter"""
    if not token:
        return "⚠️ Harap masukkan API Token dulu."

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-5",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        r = requests.post(AGENT_API_URL, headers=headers, json=body, timeout=15)
        if r.status_code == 401:
            return "⚠️ Token salah atau tidak valid."
        elif r.status_code != 200:
            return f"⚠️ Error {r.status_code}: {r.text}"

        data = r.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "⚠️ Koneksi timeout, coba lagi."
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- History percakapan
if "history" not in st.session_state:
    st.session_state.history = []

# --- Input pesan
user_input = st.chat_input("Tulis pesan...")

if user_input:
    reply = ask_agentrouter(user_input, st.session_state.agent_token)
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("ai", reply))

# --- Tampilkan percakapan
for role, msg in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg)
