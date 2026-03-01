from pathlib import Path
import streamlit as st
from minimal_gemini import parse_protocol


st.set_page_config(page_title="PDF → Lab Protocol", layout="wide")

st.title("PDF → Lab Protocol")
st.caption("Upload a PDF and extract a 4-section lab protocol: Reagents and Solutions, Equipment, Preparation, Execution.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf","jpg","jpeg","docx","png"])
generate = st.button("Generate lab protocol", type="primary", disabled=uploaded_file is None)

if generate:
    if uploaded_file is None:
        st.error("Please upload a PDF first.")
        st.stop()

    with st.spinner("Parsing PDF…"):
        try:
            protocol_md = parse_protocol(uploaded_file, filename=uploaded_file.name,file_mime_type=uploaded_file.type)
        except Exception as e:
            st.exception(e)
            st.stop()

    if not protocol_md:
        st.warning("No text returned.")
        st.stop()

    st.subheader("Lab protocol (markdown)")
    st.code(protocol_md, language="markdown")

    st.subheader("Rendered preview")
    st.markdown(protocol_md)

    st.download_button(
        "Download protocol (.md)",
        data=protocol_md.encode("utf-8"),
        file_name=f"{Path(uploaded_file.name).stem}.lab_protocol.md",
        mime="text/markdown",
    )
