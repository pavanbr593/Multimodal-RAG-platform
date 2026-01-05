import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Knowledge Intelligence Platform",
    page_icon="🤖",
    layout="wide",
)

# ---------------- Global Styling ----------------
st.markdown(
    """
    <style>
    .question-box {
        background: #1f2937;
        padding: 14px;
        border-radius: 10px;
        color: #f9fafb;
        margin-bottom: 10px;
    }
    .answer-box {
        background: #020617;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #22c55e;
        color: #e5e7eb;
        line-height: 1.6;
    }
    .file-tag {
        background: #e5e7eb;
        color: #111827;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 13px;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("## 📄 Upload Knowledge")

    uploaded_files = st.file_uploader(
        "Upload PDFs or Images",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    if "uploaded_names" not in st.session_state:
        st.session_state.uploaded_names = []

    if st.button("Upload & Index", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            for file in uploaded_files:
                files = {"file": (file.name, file.getvalue())}
                try:
                    requests.post(f"{API_URL}/upload", files=files)
                    st.session_state.uploaded_names.append(file.name)
                except:
                    st.error(f"Failed to upload {file.name}")

            st.success("Knowledge indexed successfully.")

    if st.session_state.uploaded_names:
        st.markdown("###  Indexed Files")
        for name in st.session_state.uploaded_names:
            st.markdown(f"<span class='file-tag'>{name}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Multi-Modal RAG • Local LLM • FAISS")

# ===================== MAIN =====================
st.title(" AI Knowledge Intelligence Platform")
st.caption("Ask questions across documents and images with grounded answers.")

st.markdown("---")

# ---------------- Question Input ----------------
st.subheader(" Ask a Question")

question = st.text_input(
    "",
    placeholder="Ask something from your uploaded documents...",
)

# ---------------- Ask Button ----------------
if st.button("  Ask AI", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner(" Thinking… reasoning across your knowledge base"):
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": question},
                    timeout=120,
                )

            if response.status_code != 200:
                raise RuntimeError("Backend error")

            result = response.json()

            # ----------- Q&A Layout -----------
            st.markdown("###  Question")
            st.markdown(
                f"<div class='question-box'>{question}</div>",
                unsafe_allow_html=True,
            )

            st.markdown("###  Answer")
            st.markdown(
                f"""
                <div class='answer-box'>
                {result.get("answer", "I couldn’t find enough information to answer this clearly.")}
                </div>
                """,
                unsafe_allow_html=True,
            )

        except requests.exceptions.ConnectionError:
            st.warning(
                "🤖 AI engine is starting or temporarily unavailable. "
                "Please wait a few seconds and try again."
            )

        except requests.exceptions.Timeout:
            st.warning(
                "🤖 This request is taking longer than expected. "
                "Try simplifying your question."
            )

        except Exception:
            st.warning(
                "🤖 I couldn’t generate an answer this time. "
                "Try rephrasing the question or uploading more documents."
            )