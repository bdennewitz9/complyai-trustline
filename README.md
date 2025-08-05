# ComplyAI – Trustline MVP

An enterprise-grade, modular AI scanner built for HR and legal teams. ComplyAI detects workplace compliance risks and delivers audit-ready, legally defensible guidance—right from your browser.

## 🔍 What It Does

Trustline scans submitted text for issues across five regulatory modules:

- **Anti-Harassment**
- **Whistleblower Protection**
- **EEOC Violations**
- **ADA Discrimination**
- **DEI Language Sensitivity**

Each scan returns:

- ✅ Risk flags with descriptions and rewrite guidance
- 📊 Scoring breakdown (per module and total)
- 📜 Regulatory citations to support each flag
- 🧠 Calibration suite to test performance against real-world samples

## 🚀 Try It Live

Use the public app hosted on Streamlit:  
[🔗 Launch ComplyAI Trustline](https://trustline.streamlit.app)

## 📂 How to Use Locally

1. Clone this repo
2. Run: `streamlit run streamlit_app.py`
3. Paste any workplace policy, report, or incident summary
4. Review flagged risks, scoring, and rewrite guidance
5. Compare outputs to test samples in `samples/` or `edge_cases/`

## 🧩 Modular Design

Each module runs independently and can be extended with new risk types or rulesets. Future plans include:

- 📚 Upload support (PDFs, DOCX)
- 🧾 Exportable audit logs
- 🔗 Slack and email flag triggers

## ⚙️ Requirements

See [`requirements.txt`](./requirements.txt) for dependencies.  
Key packages include:

- `streamlit`, `openai`, `scikit-learn`, `plotly`, `requests`, `tqdm`, `regex`

## 🧠 About the Builder

ComplyAI is designed and built by Brandon Dennewitz, a solo founder obsessed with modular infrastructure, legal defensibility, and making AI explainable to real-world teams. You’re not just scanning text—you’re building trust.
