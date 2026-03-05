import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Knowledge Intelligence Platform",
    page_icon="",
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
    st.markdown("##  Upload Knowledge")

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
                    resp = requests.post(f"{API_URL}/upload", files=files, timeout=60)
                    if resp.status_code == 200:
                        st.session_state.uploaded_names.append(file.name)
                    else:
                        st.error(f"Failed to upload {file.name}: {resp.text}")
                except Exception as e:
                    st.error(f"Failed to upload {file.name}: {e}")

            if st.session_state.uploaded_names:
                st.success("Knowledge indexed successfully.")

    if st.session_state.uploaded_names:
        st.markdown("### Indexed Files")
        for name in st.session_state.uploaded_names:
            st.markdown(
                f"<span class='file-tag'>{name}</span>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.caption("Multi-Modal RAG • Local LLM • FAISS")

# ===================== MAIN =====================
st.title(" AI Knowledge Intelligence Platform")
st.caption("Ask questions across documents and images with grounded answers.")

st.markdown("---")

# ---------------- Question Input ----------------
st.subheader(" Ask a Question")

question = st.text_input(
    "Question",
    placeholder="Ask something from your uploaded documents...",
    label_visibility="collapsed",
)

# ---------------- Ask Button ----------------
if st.button("Ask AI", use_container_width=True):
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

            # Handle non-200 responses
            if response.status_code != 200:
                st.error(f"Backend error ({response.status_code}): {response.text}")
                st.stop()

            # Parse JSON safely
            try:
                result = response.json()
            except Exception:
                st.error("Backend returned an invalid JSON response:")
                st.text(response.text)
                st.stop()

            answer = result.get("answer")
            if not answer:
                st.warning("The AI did not return an answer. Check backend logs.")
            else:
                # ----------- Q&A Layout -----------
                st.markdown("###  Question")
                st.markdown(
                    f"<div class='question-box'>{question}</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("###  Answer")
                st.markdown(
                    f"<div class='answer-box'>{answer}</div>",
                    unsafe_allow_html=True,
                )

        except requests.exceptions.ConnectionError:
            st.warning(
                " AI engine is starting or unavailable. "
                "Please wait a few seconds and try again."
            )

        except requests.exceptions.Timeout:
            st.warning(
                " This request took too long. "
                "Try simplifying your question."
            )

        except Exception as e:
            st.warning(f" I couldn’t generate an answer this time. Exception: {e}")
