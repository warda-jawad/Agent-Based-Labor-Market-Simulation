# app.py
import streamlit as st
import matplotlib.pyplot as plt
from model import generate_agents, LaborMarket, run_simulation

# ---------------- SESSION STATE ----------------
if "simulation_ran" not in st.session_state:
    st.session_state.simulation_ran = False
    st.session_state.timeline = None
    st.session_state.agent_summary = None

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

# ---------------- RUN SIMULATION (ONLY WHEN BUTTON IS CLICKED) ----------------
if run_button:
    agents = generate_agents(num_agents)
    labor_market = LaborMarket(jobs_per_round, market_difficulty)
    timeline, agent_summary = run_simulation(agents, labor_market, rounds)

    st.session_state.simulation_ran = True
    st.session_state.timeline = timeline
    st.session_state.agent_summary = agent_summary

# ---------------- SHOW RESULTS IF SIMULATION EXISTS ----------------
if st.session_state.simulation_ran:

    timeline = st.session_state.timeline
    agent_summary = st.session_state.agent_summary

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Agents", len(agent_summary))
    col2.metric("Employed", agent_summary["employed"].sum())
    col3.metric(
        "Employment Rate",
        f"{agent_summary['employed'].mean() * 100:.1f}%"
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

    # ======================================================
    # 👤 PERSONAL EMPLOYMENT PREDICTION
    # ======================================================

    st.divider()
    st.header("👤 Personal Employment Prediction")

    st.markdown(
        """
        Enter your personal characteristics below.
        Your employment probability is estimated using the **same logic**
        applied to agents in the simulation.
        """
    )

    with st.form("user_prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            education = st.selectbox(
                "Education Level",
                options=[0, 1, 2, 3],
                format_func=lambda x: {
                    0: "No formal education",
                    1: "High school",
                    2: "Bachelor",
                    3: "Master / PhD"
                }[x]
            )

            experience = st.slider(
                "Years of Work Experience",
                0.0, 5.0, 1.5, step=0.5
            )

            skills = st.slider(
                "Technical Skills Level",
                0.0, 1.0, 0.6
            )

        with col2:
            job_search_intensity = st.slider(
                "Job Search Intensity",
                0.0, 1.0, 0.7
            )

            digital_presence = st.slider(
                "Digital Presence (LinkedIn, Portfolio, etc.)",
                0.0, 1.0, 0.6
            )

        predict_btn = st.form_submit_button("🔮 Predict Employment Outcome")

    if predict_btn:
        user_job_potential = (
            0.3 * skills +
            0.3 * (education / 3) +
            0.2 * (experience / 5) +
            0.2 * digital_presence
        )

        user_job_potential = min(1.0, user_job_potential)
        estimated_probability = user_job_potential * (1 - market_difficulty)

        st.subheader("📊 Prediction Results")

        col1, col2 = st.columns(2)

        col1.metric(
            "Job Potential Score",
            f"{user_job_potential:.2f}"
        )

        col2.metric(
            "Estimated Employment Probability",
            f"{estimated_probability * 100:.1f}%"
        )

        if estimated_probability >= 0.6:
            st.success(
                "✅ High probability of employment under current market conditions."
            )
        elif estimated_probability >= 0.4:
            st.warning(
                "⚠️ Moderate employment chances. Improving skills or visibility may help."
            )
        else:
            st.error(
                "❌ Low employment probability. Market conditions or personal factors are limiting."
            )
