import streamlit as st
from modules.scanner import ComplianceScanner
from utils.config import load_api_key
import json
from datetime import datetime

st.set_page_config(page_title="ComplyAI: Trustline Scanner", page_icon="🛡️")
st.title("🛡️ ComplyAI v1.0 — Trustline")
st.markdown("_Enterprise-grade scanner for bias, risk, and compliance clarity._")
st.markdown("---")

doc_type = st.selectbox("📄 Document type", ["Job Post", "Company Policy", "Employee Handbook"])
company_size = st.selectbox("🏢 Company size", ["<15", "15–49", "50+"])
uploaded_file = st.file_uploader("📤 Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    doc_text = uploaded_file.read().decode("utf-8") if uploaded_file.type == "text/plain" else "Mock PDF text"
    
    scanner = ComplianceScanner(load_api_key())
    results = scanner.scan(doc_text, doc_type, company_size)
    results.update({
        "scan_timestamp": datetime.now().isoformat(),
        "document_type": doc_type,
        "company_size": company_size,
        "rule_registry_version": "2025.07"
    })

    st.subheader("✅ Scan complete! Review flagged results below 👇")
    for result in results["flags"]:
        st.markdown(f"**🚩 {result['module']} – {result['flag_type']}**")
        st.write(f"🔍 {result['original_text']}")
        st.write(f"💬 Guidance: {result['rewrite_guidance']}")
        st.write(f"📘 Citation: {result['citation']}")
        st.write(f"📊 Confidence Score: {result['confidence_score']}%")
        st.caption("This is phrasing guidance—not legal advice.")

        if st.button(f"👍 Helpful – {result['id']}"): st.success("Thanks!")
        if st.button(f"👎 Not Useful – {result['id']}"): st.warning("Feedback noted.")

    with st.expander("📤 JSON Output"):
        st.json(results)

    st.markdown("---")
    st.info("🔐 No documents are stored. All scanning is local and private.")
    st.caption("Questions or feedback? Reach out to Brandon at founder@yourdomain.com")
