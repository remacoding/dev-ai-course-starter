import asyncio

import streamlit as st

from src.config import config
from src.services.ai_service import ask_with_mcp_tool, installed_models


def format_tool_activity(result: dict) -> str:
    """Formats the tool call details for the 'Tool activity' panel."""
    if result["status"] != "ok":
        return "No tool execution."
    return (
        f"**Tool:** `{result['tool']}`\n\n"
        f"**Arguments:** `{result['arguments']}`\n\n"
        f"**Result:** `{result['observation']}`\n\n"
        f"**Execution route:** {result['route']}"
    )


async def chat_reply(message, history, model_id):
    result = await ask_with_mcp_tool(message, model_id=model_id)
    if result["status"] == "error":
        return result["message"], "No tool execution."
    return result["reply"].answer, format_tool_activity(result)


def render() -> None:
    """
    Constructs the Streamlit web interface.

    Architectural Principle: The UI communicates strictly with the AI service
    layer (`src/services/ai_service.py`) and never directly with Ollama or the
    model client.
    """
    st.set_page_config(
        page_title="Data Analysis Assistant",
        page_icon="🎓",
        layout="wide",
    )
    st.title("Data Analysis Assistant")

    models = asyncio.run(installed_models())
    if not models:
        st.error("No Ollama models are installed.")
        st.stop()

    # Start on the configured model if installed (Ollama lists names with tags)
    default = next(
        (i for i, m in enumerate(models) if m.startswith(config.model_name)), 0
    )
    model_id = st.selectbox("Model", options=models, index=default)

    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("tool_activity", "No tool execution.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if message := st.chat_input("Ask about a product..."):
        st.session_state.messages.append({"role": "user", "content": message})
        with st.chat_message("user"):
            st.markdown(message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, activity = asyncio.run(
                        chat_reply(message, st.session_state.messages[:-1], model_id)
                    )
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.tool_activity = activity
                except Exception as e:
                    st.error(f"Error: {e}")

    with st.expander("Tool activity", expanded=False):
        st.markdown(st.session_state.tool_activity)