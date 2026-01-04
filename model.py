import random
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)


class JobSeekerAgent:
    def __init__(self, agent_id, attributes):
        self.agent_id = agent_id

        # Observable attributes
        self.education = attributes.get("education")
        self.skills = attributes.get("skills")
        self.experience = attributes.get("experience")
        self.job_search_intensity = attributes.get("job_search_intensity")
        self.digital_presence = attributes.get("digital_presence")

        # Latent attribute
        self.job_potential = attributes.get("job_potential")

        # State
        self.employed = False
        self.round_hired = None

        # Data validation
        assert 0 <= self.job_search_intensity <= 1
        assert 0 <= self.job_potential <= 1

    def apply_for_jobs(self):
        if self.employed:
            return False
        return random.random() < self.job_search_intensity


class LaborMarket:
    def __init__(self, jobs_per_round, market_difficulty):
        self.jobs_per_round = jobs_per_round
        self.market_difficulty = market_difficulty

    def evaluate_applicants(self, applicants):
        hired_agents = []
        random.shuffle(applicants)

        for agent in applicants:
            if len(hired_agents) >= self.jobs_per_round:
                break

            effective_difficulty = self.market_difficulty + random.uniform(-0.05, 0.05)
            effective_difficulty = min(max(effective_difficulty, 0), 1)

            hiring_probability = agent.job_potential * (1 - effective_difficulty)

            if random.random() < hiring_probability:
                hired_agents.append(agent)

        return hired_agents


def generate_agents(num_agents):
    agents = []

    for i in range(num_agents):
        attributes = {
            "education": random.choice([0, 1, 2, 3]),
            "skills": random.uniform(0.2, 1.0),
            "experience": random.uniform(0, 5),
            "job_search_intensity": random.uniform(0.3, 1.0),
            "digital_presence": random.uniform(0.2, 1.0)
        }

        job_potential = (
            0.3 * attributes["skills"] +
            0.3 * (attributes["education"] / 3) +
            0.2 * (attributes["experience"] / 5) +
            0.2 * attributes["digital_presence"]
        )

        attributes["job_potential"] = min(1.0, job_potential)
        agents.append(JobSeekerAgent(i, attributes))

    return agents


def run_simulation(agents, labor_market, max_rounds=12):
    results = []

    for current_round in range(1, max_rounds + 1):
        applicants = [a for a in agents if a.apply_for_jobs()]
        hired_agents = labor_market.evaluate_applicants(applicants)

        for agent in hired_agents:
            agent.employed = True
            agent.round_hired = current_round

        employed_count = sum(a.employed for a in agents)

        results.append({
            "round": current_round,
            "employed_agents": employed_count,
            "unemployed_agents": len(agents) - employed_count,
            "employment_rate": employed_count / len(agents)
        })

        if employed_count == len(agents):
            break

    # ✅ MUST be inside the function
    agent_summary = pd.DataFrame([
        {
            "agent_id": a.agent_id,
            "employed": a.employed,
            "round_hired": a.round_hired,
            "job_potential": a.job_potential
        }
        for a in agents
    ])

    timeline = pd.DataFrame(results)

    return timeline, agent_summary


