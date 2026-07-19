import streamlit as st
from pdfreader import extract_text_from_pdf
from summarizer import summarize_text

st.title("📄 Research Paper Summarizer (Groq AI)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded!")

    text = extract_text_from_pdf(uploaded_file)

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(text)

        st.subheader("Summary")
        st.write(summary)