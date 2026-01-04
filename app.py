# app.py
import streamlit as st
import matplotlib.pyplot as plt
from model import generate_agents, LaborMarket, run_simulation

st.set_page_config(
    page_title="Labor Market Simulation",
    layout="wide"
)

# ---------- HEADER ----------
st.title("📊 Agent-Based Labor Market Simulation")
st.markdown("""
**Veri Bilimleri Projesi**
This dashboard simulates employment dynamics using agent-based modeling.
""")

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Simulation Parameters")

num_agents = st.sidebar.slider("Number of Agents", 50, 500, 200)
jobs_per_round = st.sidebar.slider("Jobs per Round", 5, 50, 15)
market_difficulty = st.sidebar.slider("Market Difficulty", 0.0, 1.0, 0.4)
rounds = st.sidebar.slider("Simulation Rounds", 5, 20, 12)

run_button = st.sidebar.button("▶ Run Simulation")

# ---------- RUN ----------
if run_button:
    agents = generate_agents(num_agents)
    market = LaborMarket(jobs_per_round, market_difficulty)
    timeline, summary = run_simulation(agents, market, rounds)

    # ---------- KPI CARDS ----------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Agents", num_agents)
    col2.metric("Employed", summary["employed"].sum())
    col3.metric("Employment Rate", f"{summary['employed'].mean()*100:.1f}%")

    # ---------- CHARTS ----------
    st.subheader("📈 Employment Over Time")

    fig, ax = plt.subplots()
    ax.plot(timeline["round"], timeline["employed"])
    ax.set_xlabel("Round")
    ax.set_ylabel("Employed Agents")
    st.pyplot(fig)

    st.subheader("🎯 Job Potential vs Employment")

    fig2, ax2 = plt.subplots()
    ax2.hist(summary[summary["employed"]]["job_potential"], alpha=0.6, label="Employed")
    ax2.hist(summary[~summary["employed"]]["job_potential"], alpha=0.6, label="Unemployed")
    ax2.legend()
    st.pyplot(fig2)

    # ---------- DATA ----------
    st.subheader("📄 Agent-Level Results")
    st.dataframe(summary)

    st.download_button(
        "⬇ Download Results as CSV",
        summary.to_csv(index=False),
        file_name="simulation_results.csv"
    )
