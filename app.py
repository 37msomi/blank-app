import streamlit as st

st.set_page_config(
    page_title="Production Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 Production Analytics Suite")
st.markdown("""
Welcome to your production analytics platform! Select a dashboard from the menu on the left:

- **🏭 Production Simulator** — Monte Carlo analysis for capacity planning
- **📈 AI Job Market Impact** — Analyze global job transformation trends

Each dashboard includes interactive simulations, real-time visualizations, and actionable insights.
""")

st.info("👈 Use the sidebar menu to navigate between dashboards")
