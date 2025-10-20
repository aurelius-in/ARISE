import io
from pathlib import Path

import streamlit as st

from src.core.pipeline import run_simulation
from src.core.reporting import make_pdf_report


ASSETS = Path(__file__).parent / "assets"

st.set_page_config(page_title="ARISE", page_icon="🧬", layout="wide")

# Branding header
col_logo, col_title = st.columns([1, 4])
with col_logo:
    logo_path = ASSETS / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown("<div class='logo-fallback'>ARISE</div>", unsafe_allow_html=True)
with col_title:
    st.markdown(
        """
        <h1 style="margin-bottom:0">ARISE</h1>
        <p style="margin-top:4px;color:#567">Aging Reversal In-Silico Evaluation</p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr/>", unsafe_allow_html=True)

# Sidebar options
st.sidebar.header("Run settings")
n_candidates = st.sidebar.slider("Number of virtual candidates", 20, 2000, 200, step=20)
seed = st.sidebar.number_input("Random seed", value=7, step=1)
demo = st.sidebar.checkbox("Use demo candidates", value=True)

st.sidebar.markdown("### Upload candidates (optional)")
st.sidebar.caption("CSV columns: name, type, dose, pulse_hours, target_genes")
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"]) if not demo else None

st.subheader("1) Generate predictions")
df_state_key = "arise_df"
if st.button("Run simulation"):
    with st.spinner("Simulating virtual interventions..."):
        df = run_simulation(n=n_candidates, seed=seed, csv_file=uploaded)
        st.session_state[df_state_key] = df
        st.success(f"Simulated {len(df)} candidates")
        st.dataframe(df.head(20), use_container_width=True)

df = st.session_state.get(df_state_key)
if df is not None:
    st.subheader("2) Build clinician report")
    top_k = st.number_input("How many top candidates to include", 5, 100, 20, step=5)
    pdf_bytes, csv_bytes, out_name = make_pdf_report(df, top_k=int(top_k))

    st.download_button("Download PDF report", data=pdf_bytes, file_name=out_name + ".pdf", mime="application/pdf")
    st.download_button("Download CSV data", data=csv_bytes, file_name=out_name + ".csv", mime="text/csv")
else:
    st.info("Click 'Run simulation' to generate a ranked set of therapy candidates and a clinician-ready PDF.")

st.markdown(
    """
<style>
.logo-fallback{font-size:28px;font-weight:800;color:#123}
:root{ --brand:#0E2A3E; --accent:#2B7BBB; }
h1,h2,h3{color:var(--brand)}
.stButton>button{background:var(--accent);color:white;border-radius:10px;font-weight:700}
</style>
""",
    unsafe_allow_html=True,
)


