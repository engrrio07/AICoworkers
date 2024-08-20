import streamlit as st
from crewai import Agent, Task, Crew
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Coworkers", page_icon="🤖", layout="wide")

# Initialize session state variables
if 'agents' not in st.session_state:
    st.session_state.agents = []

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.title("AI Coworkers")
st.write("Build your ideal AI crew to help with any task!")

# Function to optimize agent prompts
def optimize_agent_prompts(agents):
    crew_description = "\n".join([f"{agent.role}: {agent.goal}" for agent in agents])
    
    prompt = f"""Given the following AI crew:
    {crew_description}

    Optimize the prompts for each agent to work effectively together. For each agent, provide:
    1. An optimized goal
    2. A refined role description
    3. A backstory that complements the crew

    Format the response as a Python dictionary with agent names as keys and dictionaries containing 'goal', 'role', and 'backstory' as values."""

    client = OpenAI()

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AI assistant specializing in optimizing AI agent configurations."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return eval(response.choices[0].message['content'])

# Agent Templates
agent_templates = {
    "Researcher": {"role": "Research Specialist", "goal": "Conduct thorough research on given topics"},
    "Writer": {"role": "Content Creator", "goal": "Produce high-quality written content"},
    "Analyst": {"role": "Data Analyst", "goal": "Analyze data and provide insights"}
}

# Sidebar for adding agents
st.sidebar.header("Add New Agent")
selected_template = st.sidebar.selectbox("Choose a template (optional)", ["Custom"] + list(agent_templates.keys()))
agent_role = st.sidebar.text_input("Agent Role", help="Define the role of your AI agent")
if selected_template != "Custom":
    agent_goal = agent_templates[selected_template]["goal"]
else:
    agent_goal = st.sidebar.text_area("Agent Goal", help="Describe the main goal of your AI agent")

if st.sidebar.button("Add Agent"):
    new_agent = Agent(
        role=agent_role,
        goal=agent_goal,
        # backstory=agent_backstory,
        verbose=True
    )
    st.session_state.agents.append(new_agent)
    st.sidebar.success(f"Agent {agent_role} added!")
    
    # Optimize prompts when a new agent is added
    if len(st.session_state.agents) > 1:
        with st.spinner("Optimizing agent prompts..."):
            optimized_agents = optimize_agent_prompts(st.session_state.agents)
            for agent in st.session_state.agents:
                if agent.role in optimized_agents:
                    agent.goal = optimized_agents[agent.role]['goal']
                    agent.role = optimized_agents[agent.role]['role']
                    agent.backstory = optimized_agents[agent.role]['backstory']
        st.success("Agent prompts optimized!")

# Display added agents
st.header("Your AI Crew")
if st.session_state.agents:
    for i, agent in enumerate(st.session_state.agents):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{agent.role}**")
            st.write(f"Goal: {agent.goal}")
            st.write(f"Backstory: {agent.backstory}")
        with col2:
            if st.button(f"Delete Agent {i}"):
                if agent in [task.agent for task in st.session_state.tasks]:
                    st.error("Cannot delete agent assigned to tasks.")
                else:
                    st.session_state.agents.pop(i)
                    st.rerun()
        st.write("---")
else:
    st.write("No agents added yet.")

# Area for adding tasks
st.header("Add Tasks")
task_description = st.text_area("Task Description", help="Describe the task you want your AI agent to perform")
if st.session_state.agents:
    selected_agent = st.selectbox("Assign to Agent", options=[agent.role for agent in st.session_state.agents])
    if st.button("Add Task"):
        new_task = Task(
            description=task_description,
            agent=[agent for agent in st.session_state.agents if agent.role == selected_agent][0]
        )
        st.session_state.tasks.append(new_task)
        st.success("Task added!")
else:
    st.warning("Please add at least one agent before creating tasks.")

# Display added tasks
if st.session_state.tasks:
    st.subheader("Current Tasks")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Task**: {task.description}")
            st.write(f"Assigned to: {task.agent.role}")
        with col2:
            if st.button(f"Delete Task {i}"):
                st.session_state.tasks.pop(i)
                st.rerun()
        st.write("---")

# Button to run the crew
if st.button("Run Crew"):
    if st.session_state.agents and st.session_state.tasks:
        crew = Crew(
            agents=st.session_state.agents,
            tasks=st.session_state.tasks,
            verbose=2
        )
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Crew is working..."):
            try:
                result = crew.kickoff()
                for i, step in enumerate(crew.steps):
                    progress = (i + 1) / len(crew.steps)
                    progress_bar.progress(progress)
                    status_text.text(f"Step {i+1}/{len(crew.steps)}: {step}")
                
                st.success("Crew has completed the tasks!")
                st.subheader("Results")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please add at least one agent and one task before running the crew.")