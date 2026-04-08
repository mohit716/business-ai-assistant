import streamlit as st
import anthropic
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Business AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ── Anthropic client ──────────────────────────────────────────────────────────
import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a helpful AI assistant for a small business team.
You help employees with tasks like:
- Drafting emails and follow-ups
- Summarizing information
- Answering business questions
- Creating reports and documents
- Planning and organizing tasks
Keep responses clear, concise, and actionable."""

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🤖 Business AI Assistant")
st.caption("Ask me anything — emails, summaries, planning, reports.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Claude response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            reply = response.content[0].text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
