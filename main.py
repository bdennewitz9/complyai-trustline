import streamlit as st
from modules.scanner import ComplianceScanner
from utils.config import load_api_key
from datetime import datetime
import pdfplumber
import json

st.set_page_config(page_title="ComplyAI: Trustline Scanner", page_icon="🛡️", layout="centered")
st.title("🛡️ ComplyAI v1.0 — Trustline")
st.markdown("_Enterprise-grade scanner for bias, risk, and compliance clarity._")
st.markdown("---")

doc_type = st.selectbox("📄 Document type", ["Job Post", "Company Policy", "Employee Handbook"])
company_size = st.selectbox("🏢 Company size", ["<15", "15–49", "50+"])
uploaded_file = st.file_uploader("📤 Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file and st.button("🔍 Run Scan"):
    # Read file contents
    if uploaded_file.type == "text/plain":
        doc_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            doc_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        doc_text = "Unsupported file format."

    # Initialize scanner
    scanner = ComplianceScanner(load_api_key())
    
    if not scanner.registry:
        st.warning("⚠️ compliance_registry.json not found. Results may be incomplete.")

    results = scanner.scan(doc_text, doc_type, company_size)
    results.update({
        "scan_id": results.get("scan_id", "unknown"),
        "scan_timestamp": datetime.now().isoformat(),
        "document_type": doc_type,
        "company_size": company_size,
        "rule_registry_version": scanner.registry.get("registry_version", "unversioned")
    })

    st.subheader("✅ Scan complete! Review flagged results below 👇")
    for result in results["flags"]:
        st.markdown(f"**🚩 {result['module']} – {result['flag_type']}**")
        st.write(f"🔍 Sentence: {result['flagged_sentence']}")
        st.write(f"💬 Guidance: {result['rewrite_guidance']}")
        st.write(f"✍️ Suggested Rewrite: {result['suggested_rewrite']}")
        st.write(f"📘 Citation: {result['citation']}")
        st.write(f"📊 Confidence Score: {result['confidence_score']}%")
        st.caption("This is phrasing guidance—not legal advice.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👍 Helpful — {result['id']}"): st.success("Thanks!")
        with col2:
            if st.button(f"👎 Not Useful — {result['id']}"): st.warning("Feedback noted.")

    with st.expander("📤 JSON Output"):
        st.json(results)

    st.markdown("---")
    st.info("🔐 No documents are stored. All scanning is local and private.")
    st.caption("Questions or feedback? Reach out to Brandon at founder@yourdomain.com")
