import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📦 Supply Chain Monte Carlo Simulator")

st.markdown("Simulate stockout risk and service levels under uncertainty.")

# --- User Inputs ---
st.sidebar.header("Input Parameters")

avg_demand = st.sidebar.slider("Average Daily Demand", 50, 500, 200)
demand_std = st.sidebar.slider("Demand Variability (Std Dev)", 5, 100, 30)

lead_time = st.sidebar.slider("Average Lead Time (days)", 1, 30, 7)
lead_time_std = st.sidebar.slider("Lead Time Variability", 1, 10, 2)

safety_stock = st.sidebar.slider("Safety Stock", 0, 1000, 300)

num_simulations = st.sidebar.slider("Number of Simulations", 1000, 20000, 5000)

# --- Monte Carlo Simulation ---
stockouts = 0
final_inventory = []

for _ in range(num_simulations):
    simulated_demand = np.random.normal(avg_demand, demand_std, lead_time)
    total_demand = simulated_demand.sum()
    
    inventory = safety_stock - total_demand
    
    final_inventory.append(inventory)
    
    if inventory < 0:
        stockouts += 1

# --- Metrics ---
stockout_prob = stockouts / num_simulations
service_level = 1 - stockout_prob

st.subheader("📊 Key Results")
st.metric("Stockout Probability", f"{stockout_prob:.2%}")
st.metric("Service Level", f"{service_level:.2%}")

# --- Plot ---
st.subheader("📈 Inventory Distribution")

fig, ax = plt.subplots()
ax.hist(final_inventory, bins=50)
ax.axvline(0)
ax.set_xlabel("Ending Inventory")
ax.set_ylabel("Frequency")

st.pyplot(fig)