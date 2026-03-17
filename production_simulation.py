import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Page configuration
st.set_page_config(
    page_title="Production Capacity Simulator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏭 Production Throughput & Capacity Planning Simulator")
st.markdown("""
    **Monte Carlo simulation for factory optimization**
    
    Simulate real-world variability in machine downtime, cycle times, and operator performance 
    to understand production capacity and meeting demand targets.
""")

# ============ SIDEBAR: SIMULATION PARAMETERS ============
st.sidebar.header("⚙️ Simulation Parameters")

# Basic production parameters
num_machines = st.sidebar.number_input("Number of Machines", min_value=1, max_value=20, value=5)
num_operators = st.sidebar.number_input("Number of Operators", min_value=1, max_value=20, value=5)
num_simulations = st.sidebar.slider("Monte Carlo Simulations", min_value=100, max_value=10000, value=1000, step=100)
simulation_days = st.sidebar.slider("Simulation Period (days)", min_value=5, max_value=365, value=30, step=5)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Production Metrics")

# Cycle time parameters (minutes)
avg_cycle_time = st.sidebar.number_input("Avg Cycle Time (min)", min_value=1, max_value=120, value=30)
cycle_time_std = st.sidebar.number_input("Cycle Time Std Dev (min)", min_value=0, max_value=30, value=5)

# Downtime parameters
downtime_rate = st.sidebar.slider("Machine Downtime Rate (%)", min_value=0, max_value=50, value=15) / 100
avg_downtime_duration = st.sidebar.number_input("Avg Downtime Duration (min)", min_value=5, max_value=240, value=45)

# Operator performance
operator_efficiency = st.sidebar.slider("Operator Efficiency (%)", min_value=50, max_value=120, value=85) / 100
shift_hours = st.sidebar.slider("Shift Duration (hours)", min_value=4, max_value=24, value=8)

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Demand Target")
daily_demand = st.sidebar.number_input("Daily Demand (units)", min_value=10, max_value=1000, value=200)

# ============ SIMULATION LOGIC ============

@st.cache_data(ttl=3600)
def run_production_simulation_base(num_machines, num_operators, num_simulations, simulation_days, 
                                   avg_cycle_time, cycle_time_std, downtime_rate, avg_downtime_duration,
                                   operator_efficiency, shift_hours):
    """
    Vectorized Monte Carlo simulation for production capacity planning
    Returns raw daily outputs (independent of demand target)
    """
    
    minutes_per_day = shift_hours * 60
    np.random.seed(42)
    
    # Vectorized approach: generate all random numbers at once
    total_days = num_simulations * simulation_days
    
    # Generate downtime events for all days
    downtime_events = np.random.poisson(num_machines * downtime_rate, size=total_days)
    
    # Generate downtime durations
    downtime_durations_per_day = [np.random.exponential(avg_downtime_duration, size=int(events)) 
                                  for events in downtime_events]
    total_downtime_per_day = np.array([sum(durations) for durations in downtime_durations_per_day])
    
    # Calculate available time
    available_time = np.maximum(minutes_per_day - total_downtime_per_day, 0)
    
    # Generate cycle times (vectorized)
    cycle_times = np.random.normal(avg_cycle_time, cycle_time_std, size=total_days)
    cycle_times = np.maximum(cycle_times, 1)
    
    # Calculate daily output
    units_per_machine = available_time / cycle_times
    daily_outputs = (units_per_machine * num_operators * operator_efficiency * num_machines).astype(int)
    
    # Reshape into simulations
    daily_outputs = daily_outputs.reshape(num_simulations, simulation_days)
    
    # Calculate weekly totals
    weekly_outputs = np.array([np.sum(daily_outputs[i, :7] if simulation_days >= 7 else daily_outputs[i, :]) 
                               for i in range(num_simulations)])
    
    return daily_outputs, weekly_outputs, downtime_events.reshape(num_simulations, simulation_days)


def calculate_metrics(daily_outputs, weekly_outputs, downtime_events, daily_demand, num_simulations, simulation_days):
    """
    Fast metric calculation based on cached simulation data
    """
    results = {
        'daily_output': daily_outputs.flatten(),
        'weekly_output': weekly_outputs,
        'demand_met': np.mean(daily_outputs >= daily_demand, axis=1),  # Vectorized
        'capacity_utilization': np.mean(daily_outputs, axis=1) / daily_demand if daily_demand > 0 else np.zeros(num_simulations),
        'downtime_events': np.mean(downtime_events, axis=1),
    }
    
    return results


def run_production_simulation(num_machines, num_operators, num_simulations, simulation_days, 
                              avg_cycle_time, cycle_time_std, downtime_rate, avg_downtime_duration,
                              operator_efficiency, shift_hours, daily_demand):
    """
    Wrapper that uses cached base simulation and recalculates metrics
    """
    daily_outputs, weekly_outputs, downtime_events = run_production_simulation_base(
        num_machines, num_operators, num_simulations, simulation_days, 
        avg_cycle_time, cycle_time_std, downtime_rate, avg_downtime_duration,
        operator_efficiency, shift_hours
    )
    
    return calculate_metrics(daily_outputs, weekly_outputs, downtime_events, 
                            daily_demand, num_simulations, simulation_days)

# Run simulation
with st.spinner("⚡ Running vectorized Monte Carlo simulation..."):
    sim_results = run_production_simulation(
        num_machines, num_operators, num_simulations, simulation_days,
        avg_cycle_time, cycle_time_std, downtime_rate, avg_downtime_duration,
        operator_efficiency, shift_hours, daily_demand
    )

# ============ KEY METRICS ============
st.subheader("📈 Key Results - At a Glance")
col1, col2, col3, col4 = st.columns(4)

avg_daily_output = np.mean(sim_results['daily_output'])
avg_weekly_output = np.mean(sim_results['weekly_output'])
prob_meet_demand = np.mean(sim_results['demand_met']) * 100
avg_utilization = np.mean(sim_results['capacity_utilization'])

with col1:
    delta_text = f"{avg_daily_output - daily_demand:+,.0f}" if daily_demand > 0 else "N/A"
    st.metric(
        "📊 Avg Daily Output",
        f"{int(avg_daily_output):,}",
        delta=delta_text,
        delta_color="normal" if avg_daily_output >= daily_demand else "off",
        help="Average units produced per day"
    )

with col2:
    st.metric(
        "📦 Avg Weekly Output",
        f"{int(avg_weekly_output):,}",
        help="Average units produced per week"
    )

with col3:
    color = "normal" if prob_meet_demand >= 80 else "off"
    st.metric(
        "🎯 Demand Met",
        f"{prob_meet_demand:.1f}%",
        delta=f"{prob_meet_demand - 100:+.1f}%" if prob_meet_demand < 100 else "On Target",
        delta_color=color,
        help="Days where output meets or exceeds demand"
    )

with col4:
    st.metric(
        "⚡ Capacity Use",
        f"{avg_utilization:.1%}",
        help="How intensively you're using capacity"
    )

# ============ VISUALIZATIONS ============

# SPECIFICATION: Distribution Visualization
# Objective: Visualize daily/weekly production output to identify typical performance,
#            variability, and ability to meet demand targets
# 
# Plot Elements:
# - Histogram Trace: 1D numeric array with nbinsx=50, RGBA color, opacity for readability
# - Reference Lines: Target (red, dashed), Mean (green, solid), Median (blue, dotted)
# - Layout: Title, axis labels, hovermode='x unified', grid & background for readability
# - Annotations: Labeled reference lines with actual values
# - Statistics: Vectorized calculations (mean, median, std dev, probability of meeting target)
# - UX: Captions below chart with key metrics

st.subheader("📊 Output Distribution Analysis")
col1, col2 = st.columns(2)

with col1:
    # Daily output distribution - Vectorized calculations
    daily_mean = np.mean(sim_results['daily_output'])
    daily_median = np.median(sim_results['daily_output'])
    daily_std = np.std(sim_results['daily_output'])
    daily_min = np.min(sim_results['daily_output'])
    daily_max = np.max(sim_results['daily_output'])
    prob_daily = np.mean(sim_results['daily_output'] >= daily_demand) * 100
    
    fig1 = go.Figure()
    
    # Histogram Trace: 1D array with transparency
    fig1.add_trace(go.Histogram(
        x=sim_results['daily_output'],
        nbinsx=50,
        name='Daily Output',
        marker_color='rgba(99, 110, 250, 0.7)',  # RGBA for transparency
        opacity=0.7,
        hovertemplate='<b>Output Range</b><br>%{x:,} units<br>Frequency: %{y}<extra></extra>'
    ))
    
    # Reference Lines with Annotations
    # Target line - RED (demand threshold)
    fig1.add_vline(x=daily_demand, line_dash="dash", line_color="#EF553B", line_width=3,
                   annotation_text=f"Target: {daily_demand:,}", annotation_position="top right",
                   annotation_font_size=11, annotation_font_color="#EF553B")
    
    # Mean line - GREEN (typical output)
    fig1.add_vline(x=daily_mean, line_dash="solid", line_color="#00CC96", line_width=3,
                   annotation_text=f"Mean: {daily_mean:,.0f}", annotation_position="top left",
                   annotation_font_size=11, annotation_font_color="#00CC96")
    
    # Median line - BLUE (center of distribution)
    fig1.add_vline(x=daily_median, line_dash="dot", line_color="#636EFA", line_width=3,
                   annotation_text=f"Median: {daily_median:,.0f}", annotation_position="bottom right",
                   annotation_font_size=11, annotation_font_color="#636EFA")
    
    # Layout configuration for readability
    fig1.update_layout(
        title="Daily Output Distribution",
        xaxis_title="Units/Day",
        yaxis_title="Frequency",
        height=450,
        hovermode='x unified',  # Combined hover for easier reading
        font=dict(size=11),
        plot_bgcolor='rgba(240, 240, 240, 0.5)',  # Subtle background
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # Grid configuration for readability
    fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white')
    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white')
    
    st.plotly_chart(fig1, width='stretch', use_container_width=True)
    
    # Insights Summary: Vectorized statistics
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.caption(f"📊 **Mean:** {daily_mean:,.0f}")
    with col_s2:
        st.caption(f"📈 **Median:** {daily_median:,.0f}")
    with col_s3:
        st.caption(f"📉 **Std Dev:** {daily_std:,.0f}")
    with col_s4:
        st.caption(f"✅ **Meet %:** {prob_daily:.1f}%")

with col2:
    # Weekly output distribution - Vectorized calculations
    weekly_mean = np.mean(sim_results['weekly_output'])
    weekly_median = np.median(sim_results['weekly_output'])
    weekly_std = np.std(sim_results['weekly_output'])
    weekly_min = np.min(sim_results['weekly_output'])
    weekly_max = np.max(sim_results['weekly_output'])
    weekly_target = daily_demand * 5
    prob_weekly = np.mean(sim_results['weekly_output'] >= weekly_target) * 100
    
    fig2 = go.Figure()
    
    # Histogram Trace: 1D array with transparency
    fig2.add_trace(go.Histogram(
        x=sim_results['weekly_output'],
        nbinsx=50,
        name='Weekly Output',
        marker_color='rgba(239, 85, 59, 0.7)',  # RGBA for transparency
        opacity=0.7,
        hovertemplate='<b>Output Range</b><br>%{x:,} units<br>Frequency: %{y}<extra></extra>'
    ))
    
    # Reference Lines with Annotations
    # Target line - RED (demand threshold)
    fig2.add_vline(x=weekly_target, line_dash="dash", line_color="#EF553B", line_width=3,
                   annotation_text=f"Target: {weekly_target:,}", annotation_position="top right",
                   annotation_font_size=11, annotation_font_color="#EF553B")
    
    # Mean line - GREEN (typical output)
    fig2.add_vline(x=weekly_mean, line_dash="solid", line_color="#00CC96", line_width=3,
                   annotation_text=f"Mean: {weekly_mean:,.0f}", annotation_position="top left",
                   annotation_font_size=11, annotation_font_color="#00CC96")
    
    # Median line - BLUE (center of distribution)
    fig2.add_vline(x=weekly_median, line_dash="dot", line_color="#636EFA", line_width=3,
                   annotation_text=f"Median: {weekly_median:,.0f}", annotation_position="bottom right",
                   annotation_font_size=11, annotation_font_color="#636EFA")
    
    # Layout configuration for readability
    fig2.update_layout(
        title="Weekly Output Distribution",
        xaxis_title="Units/Week",
        yaxis_title="Frequency",
        height=450,
        hovermode='x unified',  # Combined hover for easier reading
        font=dict(size=11),
        plot_bgcolor='rgba(240, 240, 240, 0.5)',  # Subtle background
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # Grid configuration for readability
    fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white')
    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white')
    
    st.plotly_chart(fig2, width='stretch', use_container_width=True)
    
    # Insights Summary: Vectorized statistics
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.caption(f"📊 **Mean:** {weekly_mean:,.0f}")
    with col_s2:
        st.caption(f"📈 **Median:** {weekly_median:,.0f}")
    with col_s3:
        st.caption(f"📉 **Std Dev:** {weekly_std:,.0f}")
    with col_s4:
        st.caption(f"✅ **Meet %:** {prob_weekly:.1f}%")

# Add legend explanation
st.markdown("""
<div style="background-color: #f0f0f0; padding: 12px; border-radius: 8px; margin-top: 10px;">
    <b>📍 Line Legend:</b>
    <span style="margin-left: 20px;">🔴 <b>Red (Dashed)</b> = Your target demand</span>
    <span style="margin-left: 20px;">🟢 <b>Green (Solid)</b> = Your typical output (mean)</span>
    <span style="margin-left: 20px;">🔵 <b>Blue (Dotted)</b> = Median output (center)</span>
</div>
""", unsafe_allow_html=True)

# ============ Cumulative Probability ============
st.subheader("📉 Cumulative Probability Analysis")

daily_sorted = np.sort(sim_results['daily_output'])
cumulative_prob = np.arange(1, len(daily_sorted) + 1) / len(daily_sorted)

# Find key percentiles
p10 = np.percentile(sim_results['daily_output'], 10)
p25 = np.percentile(sim_results['daily_output'], 25)
p50 = np.percentile(sim_results['daily_output'], 50)
p75 = np.percentile(sim_results['daily_output'], 75)
p90 = np.percentile(sim_results['daily_output'], 90)

# Probability of meeting demand
prob_exceed_demand = np.mean(sim_results['daily_output'] >= daily_demand) * 100

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=daily_sorted,
    y=cumulative_prob * 100,
    mode='lines',
    name='Cumulative Probability',
    line=dict(color='#00CC96', width=3)
))

# Add demand line
fig3.add_vline(x=daily_demand, line_dash="dash", line_color="red", line_width=2,
               annotation_text=f"Daily Demand: {daily_demand:,}", 
               annotation_position="top right",
               annotation_font_size=12,
               annotation_font_color="red")

# Add percentile bands
fig3.add_hline(y=10, line_dash="dot", line_color="gray", line_width=1, opacity=0.5)
fig3.add_hline(y=25, line_dash="dot", line_color="gray", line_width=1, opacity=0.5)
fig3.add_hline(y=50, line_dash="dot", line_color="gray", line_width=1, opacity=0.5)
fig3.add_hline(y=75, line_dash="dot", line_color="gray", line_width=1, opacity=0.5)
fig3.add_hline(y=90, line_dash="dot", line_color="gray", line_width=1, opacity=0.5)

fig3.update_layout(
    title="Cumulative Probability of Exceeding Output Threshold",
    xaxis_title="Daily Output (units)",
    yaxis_title="Cumulative Probability (%)",
    hovermode='x unified',
    height=500,
    font=dict(size=11),
    showlegend=False
)

st.plotly_chart(fig3, width='stretch')

# Add probability insights
col1, col2, col3 = st.columns(3)

with col1:
    p_exceed = np.mean(sim_results['daily_output'] >= daily_demand) * 100
    st.metric("🎯 Prob. of Meeting Demand", f"{p_exceed:.1f}%", 
              help="Percentage of days where output ≥ demand target")

with col2:
    p_shortfall = 100 - p_exceed
    avg_shortfall = np.mean(daily_demand - sim_results['daily_output'][sim_results['daily_output'] < daily_demand])
    st.metric("⚠️ Expected Shortfall", f"{avg_shortfall:,.0f} units",
              help="Average units short on days when demand not met")

with col3:
    p_exceed_10pct = np.mean(sim_results['daily_output'] >= daily_demand * 1.1) * 100
    st.metric("📈 Prob. of 10% Buffer", f"{p_exceed_10pct:.1f}%",
              help="Percentage of days with 10% cushion above demand")

# Add percentile reference table
st.markdown("**Percentile Reference:**")
percentile_data = {
    'Percentile': ['10th', '25th', '50th (Median)', '75th', '90th'],
    'Daily Output (units)': [f"{int(p10):,}", f"{int(p25):,}", f"{int(p50):,}", f"{int(p75):,}", f"{int(p90):,}"],
    'Interpretation': [
        'Only 10% of days below this',
        '25% of days below this',
        'Typical day output',
        '75% of days below this',
        '90% of days below this'
    ]
}

st.dataframe(pd.DataFrame(percentile_data), use_container_width=True, hide_index=True)

# ============ SCENARIO ANALYSIS ============
st.subheader("🔍 Sensitivity Analysis: What If?")

col1, col2, col3 = st.columns(3)

with col1:
    scenario_machines = st.number_input("Scenario: Add Machines", min_value=0, max_value=10, value=0, key="add_machines")

with col2:
    scenario_operators = st.number_input("Scenario: Add Operators", min_value=0, max_value=10, value=0, key="add_operators")

with col3:
    scenario_efficiency = st.slider("Scenario: New Efficiency (%)", min_value=50, max_value=120, value=85, key="efficiency") / 100

# Only run scenario if something actually changed
scenario_changed = (scenario_machines != 0) or (scenario_operators != 0) or (scenario_efficiency != operator_efficiency)

if scenario_changed and st.button("🔄 Run Scenario Simulation", key="scenario_btn"):
    with st.spinner("⚡ Running scenario (optimized)..."):
        # Get cached base simulation results
        scenario_daily_outputs, scenario_weekly_outputs, scenario_downtime_events = run_production_simulation_base(
            num_machines + scenario_machines,
            num_operators + scenario_operators,
            num_simulations, simulation_days,
            avg_cycle_time, cycle_time_std, downtime_rate, avg_downtime_duration,
            scenario_efficiency, shift_hours
        )
        
        scenario_results = calculate_metrics(scenario_daily_outputs, scenario_weekly_outputs, 
                                            scenario_downtime_events, daily_demand, 
                                            num_simulations, simulation_days)
    
    # Comparison
    col1, col2, col3, col4 = st.columns(4)
    
    baseline_demand_met = np.mean(sim_results['demand_met']) * 100
    scenario_demand_met = np.mean(scenario_results['demand_met']) * 100
    improvement = scenario_demand_met - baseline_demand_met
    
    with col1:
        st.metric("Baseline: Prob. Meeting Demand", f"{baseline_demand_met:.1f}%")
    
    with col2:
        st.metric("Scenario: Prob. Meeting Demand", f"{scenario_demand_met:.1f}%")
    
    with col3:
        st.metric("Improvement", f"{improvement:+.1f}%", delta=f"{improvement:.1f}%")
    
    with col4:
        roi_text = "✅ Worth it!" if improvement > 5 else "❌ Not significant"
        st.metric("ROI Assessment", roi_text)
    
    # Comparison visualization - improved
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Box(
        y=sim_results['daily_output'],
        name='Baseline',
        boxmean=True,
        marker_color='#636EFA'
    ))
    
    fig_compare.add_trace(go.Box(
        y=scenario_results['daily_output'],
        name='Scenario',
        boxmean=True,
        marker_color='#EF553B'
    ))
    
    fig_compare.add_hline(y=daily_demand, line_dash="dash", line_color="green", line_width=2,
                          annotation_text=f"Demand: {daily_demand:,} units",
                          annotation_position="right",
                          annotation_font_size=12,
                          annotation_font_color="green")
    
    fig_compare.update_layout(
        title=f"📊 Baseline vs. Scenario Output Comparison<br><sub>Baseline: {num_machines} machines, {num_operators} operators | Scenario: +{scenario_machines} machines, +{scenario_operators} operators, {int(scenario_efficiency*100)}% efficiency</sub>",
        yaxis_title="Daily Output (units)",
        height=500,
        font=dict(size=11),
        hovermode='y unified'
    )
    
    st.plotly_chart(fig_compare, width='stretch')

# ============ INSIGHTS & DATA TABLE ============
st.subheader("💡 Key Insights & Executive Summary")

col1, col2 = st.columns(2)

with col1:
    uncertainty = (np.std(sim_results['daily_output']) / avg_daily_output) * 100
    
    if uncertainty < 15:
        risk_level = "🟢 Low"
    elif uncertainty < 25:
        risk_level = "🟡 Medium"
    else:
        risk_level = "🔴 High"
    
    st.info(f"""
    ### 📊 Production Variability
    **Risk Level:** {risk_level}
    
    - **Range:** {int(np.min(sim_results['daily_output'])):,} to {int(np.max(sim_results['daily_output'])):,} units/day
    - **Variability:** {uncertainty:.1f}% (Std Dev / Mean)
    - **Standard Deviation:** ±{np.std(sim_results['daily_output']):,.0f} units
    
    The higher the percentage, the more variable your production is.
    """)

with col2:
    daily_shortfall = np.where(np.array(sim_results['daily_output']) < daily_demand, 
                               daily_demand - np.array(sim_results['daily_output']), 0)
    avg_shortfall = np.mean(daily_shortfall[daily_shortfall > 0]) if np.any(daily_shortfall > 0) else 0
    days_short = np.sum(daily_shortfall > 0)
    total_units_short = np.sum(daily_shortfall)
    
    if prob_meet_demand > 90:
        status = "✅ Excellent"
    elif prob_meet_demand > 80:
        status = "👍 Good"
    elif prob_meet_demand > 70:
        status = "⚠️ Marginal"
    else:
        status = "🚨 At Risk"
    
    st.info(f"""
    ### 📌 Demand Achievement
    **Status:** {status}
    
    - **Meeting Demand:** {prob_meet_demand:.1f}% of days
    - **Missing Demand:** {100-prob_meet_demand:.1f}% of days
    - **Avg Shortfall (when miss):** {avg_shortfall:,.0f} units
    - **Total Annual Shortfall:** ~{total_units_short * (365/simulation_days):,.0f} units
    
    Based on {num_simulations:,} simulations over {simulation_days} days.
    """)

st.subheader("📋 Detailed Simulation Data")
if st.checkbox("Show detailed results"):
    
    # Create summary dataframe with better formatting
    summary_data = {
        'Metric': [
            'Average Daily Output',
            'Min Daily Output (worst case)',
            'Max Daily Output (best case)',
            'Std Dev Daily Output',
            'Average Weekly Output',
            'Probability Meeting Daily Demand',
            'Average Downtime Events/Day',
            'Capacity Utilization vs Demand'
        ],
        'Value': [
            f"{avg_daily_output:,.0f} units",
            f"{int(np.min(sim_results['daily_output'])):,} units",
            f"{int(np.max(sim_results['daily_output'])):,} units",
            f"{np.std(sim_results['daily_output']):,.0f} units",
            f"{avg_weekly_output:,.0f} units",
            f"{prob_meet_demand:.1f}%",
            f"{np.mean(sim_results['downtime_events']):.2f} events",
            f"{avg_utilization:.1%}"
        ],
        'Insight': [
            'Your typical daily production',
            'Plan for this in worst scenarios',
            'Your best-case scenario',
            'Production volatility (lower is better)',
            'Typical weekly output',
            'How often you hit your target',
            'Machines breaking down per day',
            'How hard you\'re pushing capacity'
        ]
    }
    
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    **How to interpret this:**
    - If **Avg Utilization > 100%**, you're over-committed
    - If **Prob. Meeting Demand < 80%**, consider expanding capacity
    - If **Std Dev is high**, add buffer stock or extend lead times
    """)

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🏭 Production Simulator | Monte Carlo Analysis for Manufacturing Optimization</p>
    <p>Perfect for LinkedIn: Share insights about production optimization and capacity planning</p>
    </div>
""", unsafe_allow_html=True)
