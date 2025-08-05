import streamlit as st
from modules.scanner import ComplianceScanner

# Page config
st.set_page_config(page_title="ComplyAI Trustline Scanner", layout="wide")

# Sidebar upload
st.sidebar.header("📄 Upload a .txt File")
uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")

# Scanner logic
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    scanner = ComplianceScanner()
    result = scanner.scan(text)

    st.title("🧠 ComplyAI Trustline Scanner")
    st.markdown("Enterprise-grade bias detection, rewrite guidance, and audit-ready scoring.")

    st.markdown("---")

    # Original Input
    st.subheader("📄 Original Input")
    st.code(text, language="text")

    st.markdown("---")

    # Flags
    st.subheader("🚨 Flags Detected")
    if result["flags"]:
        with st.expander("View Detected Flags"):
            for flag in result["flags"]:
                st.markdown(f"- {flag}")
    else:
        st.markdown("✅ No compliance flags detected.")

    st.markdown("---")

    # Rewrite Suggestions
    st.subheader("✏️ Rewrite Suggestions")
    st.markdown(result["rewrite"] or "✅ No rewrite needed.")

    st.markdown("---")

    # Trustline Score
    st.subheader("📊 Trustline Score")
    st.metric(label="Score", value=f"{result['score']}/100")

    st.markdown("---")

    # Regulatory Tags
    st.subheader("📚 Regulatory Tags")
    if result["tags"]:
        st.markdown(", ".join([f"`{tag}`" for tag in result["tags"]]))
    else:
        st.markdown("None detected.")

    st.markdown("---")

    # Footer
    st.caption("Built by ComplyAI • Modular • Auditable • Enterprise-Ready")
else:
    st.title("🧠 ComplyAI Trustline Scanner")
    st.markdown("Upload a `.txt` file to begin scanning for compliance flags, rewrite guidance, and trustline scoring.")
