
### 📊 Agent-Based Labor Market Simulation 
An agent-based simulation that models labor market dynamics by simulating how individual job seekers interact with market conditions over time.
The project combines computational modeling, data analysis, and an interactive Streamlit UI for visualization and personal employment prediction.

### 🚀 Live Demo (Streamlit UI)

👉 Access the interactive web application here:
🔗 https://agent-based-labor-market-simulation-xjvjbboandnebox6kuxzvc.streamlit.app/

### 📌 Project Overview

This project simulates a labor market where:

- Each job seeker is modeled as an independent agent

- Agents differ in education, skills, experience, job search behavior, and digital presence

- A limited number of jobs are available in each round

- Hiring decisions are probabilistic and depend on: Agent’s job potential and Overall market difficulty

The simulation tracks:

- Employment growth over time

- Individual hiring outcomes

- Aggregate employment rates

Additionally, the UI allows personal employment prediction using the same logic applied to simulated agents.

### 🧠 Model Concept
## Agent Attributes

Each job seeker has:

|Attribute |Description |
|---------|------------|
| Education | Discrete level (0–3) |
| Skills | Continuous value (0–1) |
| Experience | Years of experience (0–5) |
| Job Search Intensity | Probability of applying each round |
| Digital Presence | Online visibility (0–1) |
| Job Potential | Latent score derived from all attributes |

### job_potential =
0.3 × skills +
0.3 × (education / 3) +
0.2 × (experience / 5) +
0.2 × digital_presence

### Hiring Probability
hiring_probability = job_potential × (1 − market_difficulty)
