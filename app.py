# app.py
import streamlit as st
import matplotlib.pyplot as plt
from model import generate_agents, LaborMarket, run_simulation

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Agent-Based Labor Market Simulation",
    layout="wide",
    page_icon="📊"
)

# ---------------- TITLE ----------------
st.title("📊 Agent-Based Labor Market Simulation")
st.caption("Veri Bilimleri Projesi — Agent-Based Modeling")

st.markdown(
    """
    This application simulates **labor market dynamics** using  
    **agent-based modeling**, where each job seeker behaves independently
    based on personal attributes and market conditions.
    """
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Simulation Parameters")

num_agents = st.sidebar.slider("Number of Agents", 50, 500, 200)
jobs_per_round = st.sidebar.slider("Jobs per Round", 5, 50, 20)
market_difficulty = st.sidebar.slider("Market Difficulty", 0.0, 1.0, 0.4)
rounds = st.sidebar.slider("Simulation Rounds", 5, 24, 12)

run_button = st.sidebar.button("▶ Run Simulation")

# ---------------- RUN SIMULATION ----------------
if run_button:
    agents = generate_agents(num_agents)
    labor_market = LaborMarket(jobs_per_round, market_difficulty)
    timeline, agent_summary = run_simulation(agents, labor_market, rounds)

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Agents", num_agents)
    col2.metric("Employed", agent_summary["employed"].sum())
    col3.metric(
        "Employment Rate",
        f"{agent_summary['employed'].mean()*100:.1f}%"
    )

    st.divider()

    # ---------------- CHART ----------------
    st.subheader("📈 Employment Over Time")

    fig, ax = plt.subplots()
    ax.plot(
        timeline["round"],
        timeline["employed_agents"],
        marker="o",
        linewidth=3
    )
    ax.set_xlabel("Round")
    ax.set_ylabel("Employed Agents")
    ax.grid(True)

    st.pyplot(fig)

    # ---------------- DATA TABLE ----------------
    with st.expander("📋 Agent-Level Results"):
        st.dataframe(agent_summary, use_container_width=True)
