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
    
    # Histogram with vibrant colors
    fig1.add_trace(go.Histogram(
        x=sim_results['daily_output'],
        nbinsx=30,
        name='Daily Output',
        marker_color='#1f77b4',  # Bold blue
        marker_line_color='#0a3d62',  # Dark blue outline
        marker_line_width=0.5,
        hovertemplate='<b>%{x:,} units</b><br>Frequency: %{y}<extra></extra>'
    ))
    
    # Add legend traces (invisible, just for legend)
    fig1.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#FF4444', width=4, dash='dash'),
        name=f'Target: {daily_demand:,}'
    ))
    
    fig1.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#00DD44', width=4, dash='solid'),
        name=f'Mean: {daily_mean:,.0f}'
    ))
    
    fig1.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#AA00FF', width=4, dash='dot'),
        name=f'Median: {daily_median:,.0f}'
    ))
    
    # Reference Lines - NO ANNOTATIONS
    # Target line - RED (demand threshold)
    fig1.add_vline(x=daily_demand, line_dash="dash", line_color="#FF4444", line_width=4)
    
    # Mean line - GREEN (typical output)
    fig1.add_vline(x=daily_mean, line_dash="solid", line_color="#00DD44", line_width=4)
    
    # Median line - PURPLE (center of distribution)
    fig1.add_vline(x=daily_median, line_dash="dot", line_color="#AA00FF", line_width=4)
    
    # Professional layout
    fig1.update_layout(
        title=f"<b>Daily Output Distribution</b><br><sub>Prob Met: {prob_daily:.0f}%</sub>",
        xaxis_title="<b>Units per Day</b>",
        yaxis_title="<b>Frequency (# of days)</b>",
        height=550,
        hovermode='x unified',
        font=dict(size=13, family="Arial, sans-serif", color="#333333"),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=80),
        xaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        yaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        legend=dict(
            x=0.98, y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#CCCCCC',
            borderwidth=1,
            font=dict(size=10, color="#333333")
        )
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Statistics with larger text
    st.write("**📊 Daily Statistics:**")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Mean", f"{daily_mean:,.0f}")
    with col_s2:
        st.metric("Median", f"{daily_median:,.0f}")
    with col_s3:
        st.metric("Std Dev", f"{daily_std:,.0f}")
    with col_s4:
        st.metric("Meet %", f"{prob_daily:.1f}%")

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
    
    # Histogram with vibrant colors (different scheme)
    fig2.add_trace(go.Histogram(
        x=sim_results['weekly_output'],
        nbinsx=30,
        name='Weekly Output',
        marker_color='#ff7f0e',  # Bold orange
        marker_line_color='#cc5500',  # Dark orange outline
        marker_line_width=0.5,
        hovertemplate='<b>%{x:,} units</b><br>Frequency: %{y}<extra></extra>'
    ))
    
    # Add legend traces (invisible, just for legend)
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#FF4444', width=4, dash='dash'),
        name=f'Target: {weekly_target:,}'
    ))
    
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#00DD44', width=4, dash='solid'),
        name=f'Mean: {weekly_mean:,.0f}'
    ))
    
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#AA00FF', width=4, dash='dot'),
        name=f'Median: {weekly_median:,.0f}'
    ))
    
    # Reference Lines - NO ANNOTATIONS
    # Target line - RED (demand threshold)
    fig2.add_vline(x=weekly_target, line_dash="dash", line_color="#FF4444", line_width=4)
    
    # Mean line - GREEN (typical output)
    fig2.add_vline(x=weekly_mean, line_dash="solid", line_color="#00DD44", line_width=4)
    
    # Median line - PURPLE (center of distribution)
    fig2.add_vline(x=weekly_median, line_dash="dot", line_color="#AA00FF", line_width=4)
    
    # Professional layout
    fig2.update_layout(
        title=f"<b>Weekly Output Distribution</b><br><sub>Prob Met: {prob_weekly:.0f}%</sub>",
        xaxis_title="<b>Units per Week</b>",
        yaxis_title="<b>Frequency (# of weeks)</b>",
        height=550,
        hovermode='x unified',
        font=dict(size=13, family="Arial, sans-serif", color="#333333"),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=80),
        xaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        yaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        legend=dict(
            x=0.98, y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#CCCCCC',
            borderwidth=1,
            font=dict(size=10, color="#333333")
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Statistics with larger text
    st.write("**📦 Weekly Statistics:**")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Mean", f"{weekly_mean:,.0f}")
    with col_s2:
        st.metric("Median", f"{weekly_median:,.0f}")
    with col_s3:
        st.metric("Std Dev", f"{weekly_std:,.0f}")
    with col_s4:
        st.metric("Meet %", f"{prob_weekly:.1f}%")

# Monthly and Yearly Analysis
st.subheader("📅 Monthly & Yearly Projections")
col3, col4 = st.columns(2)

# Calculate monthly outputs (sum of 30-day periods) and yearly (extrapolated)
# Reshape daily outputs to calculate monthly aggregations
daily_outputs_2d = sim_results['daily_output'].reshape(-1, simulation_days) if len(sim_results['daily_output'].shape) == 1 else sim_results['daily_output']
days_in_month = min(30, simulation_days)
monthly_outputs = np.array([np.sum(daily_outputs_2d[i, :days_in_month]) for i in range(len(daily_outputs_2d))])
yearly_outputs = np.array([np.sum(daily_outputs_2d[i, :]) * (365 / simulation_days) for i in range(len(daily_outputs_2d))])

with col3:
    # Monthly output distribution
    monthly_mean = np.mean(monthly_outputs)
    monthly_median = np.median(monthly_outputs)
    monthly_std = np.std(monthly_outputs)
    monthly_target = daily_demand * days_in_month
    prob_monthly = np.mean(monthly_outputs >= monthly_target) * 100
    
    fig3 = go.Figure()
    
    # Histogram
    fig3.add_trace(go.Histogram(
        x=monthly_outputs,
        nbinsx=30,
        name='Monthly Output',
        marker_color='#2ca02c',  # Green
        marker_line_color='#1a6b1a',  # Dark green outline
        marker_line_width=0.5,
        hovertemplate='<b>%{x:,} units</b><br>Frequency: %{y}<extra></extra>'
    ))
    
    # Add legend traces
    fig3.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#FF4444', width=4, dash='dash'),
        name=f'Target: {monthly_target:,}'
    ))
    
    fig3.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#00DD44', width=4, dash='solid'),
        name=f'Mean: {monthly_mean:,.0f}'
    ))
    
    fig3.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#AA00FF', width=4, dash='dot'),
        name=f'Median: {monthly_median:,.0f}'
    ))
    
    # Reference lines
    fig3.add_vline(x=monthly_target, line_dash="dash", line_color="#FF4444", line_width=4)
    fig3.add_vline(x=monthly_mean, line_dash="solid", line_color="#00DD44", line_width=4)
    fig3.add_vline(x=monthly_median, line_dash="dot", line_color="#AA00FF", line_width=4)
    
    fig3.update_layout(
        title=f"<b>Monthly Output Distribution</b><br><sub>Prob Met: {prob_monthly:.0f}%</sub>",
        xaxis_title="<b>Units per Month</b>",
        yaxis_title="<b>Frequency</b>",
        height=550,
        hovermode='x unified',
        font=dict(size=13, family="Arial, sans-serif", color="#333333"),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=80),
        xaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        yaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        legend=dict(
            x=0.98, y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#CCCCCC',
            borderwidth=1,
            font=dict(size=10, color="#333333")
        )
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.write("**📊 Monthly Statistics:**")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Mean", f"{monthly_mean:,.0f}")
    with col_m2:
        st.metric("Median", f"{monthly_median:,.0f}")
    with col_m3:
        st.metric("Std Dev", f"{monthly_std:,.0f}")
    with col_m4:
        st.metric("Meet %", f"{prob_monthly:.1f}%")

with col4:
    # Yearly output distribution
    yearly_mean = np.mean(yearly_outputs)
    yearly_median = np.median(yearly_outputs)
    yearly_std = np.std(yearly_outputs)
    yearly_target = daily_demand * 365
    prob_yearly = np.mean(yearly_outputs >= yearly_target) * 100
    
    fig4 = go.Figure()
    
    # Histogram
    fig4.add_trace(go.Histogram(
        x=yearly_outputs,
        nbinsx=30,
        name='Yearly Output',
        marker_color='#d62728',  # Red
        marker_line_color='#7f1a1a',  # Dark red outline
        marker_line_width=0.5,
        hovertemplate='<b>%{x:,} units</b><br>Frequency: %{y}<extra></extra>'
    ))
    
    # Add legend traces
    fig4.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#FF4444', width=4, dash='dash'),
        name=f'Target: {yearly_target:,}'
    ))
    
    fig4.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#00DD44', width=4, dash='solid'),
        name=f'Mean: {yearly_mean:,.0f}'
    ))
    
    fig4.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#AA00FF', width=4, dash='dot'),
        name=f'Median: {yearly_median:,.0f}'
    ))
    
    # Reference lines
    fig4.add_vline(x=yearly_target, line_dash="dash", line_color="#FF4444", line_width=4)
    fig4.add_vline(x=yearly_mean, line_dash="solid", line_color="#00DD44", line_width=4)
    fig4.add_vline(x=yearly_median, line_dash="dot", line_color="#AA00FF", line_width=4)
    
    fig4.update_layout(
        title=f"<b>Yearly Output Distribution</b><br><sub>Prob Met: {prob_yearly:.0f}%</sub>",
        xaxis_title="<b>Units per Year</b>",
        yaxis_title="<b>Frequency</b>",
        height=550,
        hovermode='x unified',
        font=dict(size=13, family="Arial, sans-serif", color="#333333"),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=100, b=80),
        xaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        yaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
        legend=dict(
            x=0.98, y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#CCCCCC',
            borderwidth=1,
            font=dict(size=10, color="#333333")
        )
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.write("**📊 Yearly Statistics:**")
    col_y1, col_y2, col_y3, col_y4 = st.columns(4)
    with col_y1:
        st.metric("Mean", f"{yearly_mean:,.0f}")
    with col_y2:
        st.metric("Median", f"{yearly_median:,.0f}")
    with col_y3:
        st.metric("Std Dev", f"{yearly_std:,.0f}")
    with col_y4:
        st.metric("Meet %", f"{prob_yearly:.1f}%")

# Add legend explanation
st.markdown("""
<div style="background-color: #f0f0f0; padding: 16px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #333;">
    <b style="font-size: 16px;">📍 Reference Line Guide</b><br><br>
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><span style="color: #FF4444; font-weight: bold;">━ ━ Dashed Red</span></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">Your demand target (what you need to hit)</td></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><span style="color: #00AA22; font-weight: bold;">━ Solid Green</span></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">Your average output (mean/typical performance)</td></tr>
        <tr><td style="padding: 8px;"><span style="color: #AA00FF; font-weight: bold;">· · Dotted Purple</span></td><td style="padding: 8px;">Median output (center of distribution)</td></tr>
    </table>
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

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=daily_sorted,
    y=cumulative_prob * 100,
    mode='lines',
    name='Cumulative Probability',
    line=dict(color='#1f77b4', width=4)
))

# Add demand line - BOLD RED
fig3.add_vline(x=daily_demand, line_dash="dash", line_color="#FF4444", line_width=4,
               annotation_text=f"<b>TARGET: {daily_demand:,}</b>", 
               annotation_position="top right",
               annotation_font_size=13,
               annotation_font_color="#FF4444",
               annotation_bgcolor="#FFF8F8")

fig3.update_layout(
    title="<b>Cumulative Probability of Meeting Output Threshold</b>",
    xaxis_title="<b>Daily Output (units)</b>",
    yaxis_title="<b>Probability (%)</b>",
    hovermode='x unified',
    height=550,
    font=dict(size=13, family="Arial, sans-serif", color="#333333"),
    showlegend=False,
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='white',
    margin=dict(l=60, r=60, t=80, b=60),
    xaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
    yaxis=dict(showgrid=True, gridwidth=2, gridcolor='#eeeeee', zeroline=False),
)

st.plotly_chart(fig3, use_container_width=True)

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

st.write("**Tweak these parameters to see how they impact your production capacity:**")

col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Resources**")
    scenario_machines = st.number_input("Add Machines", min_value=-5, max_value=10, value=0, key="add_machines")
    scenario_operators = st.number_input("Add Operators", min_value=-5, max_value=10, value=0, key="add_operators")

with col2:
    st.write("**Performance**")
    scenario_cycle_time = st.number_input("Avg Cycle Time (min)", min_value=1, max_value=120, value=int(avg_cycle_time), key="scenario_cycle_time")
    scenario_efficiency = st.slider("Operator Efficiency (%)", min_value=50, max_value=120, value=int(operator_efficiency*100), key="efficiency") / 100

with col3:
    st.write("**Operations**")
    scenario_downtime = st.slider("Machine Downtime Rate (%)", min_value=0, max_value=50, value=int(downtime_rate*100), key="scenario_downtime") / 100
    scenario_shift = st.slider("Shift Duration (hours)", min_value=4, max_value=24, value=int(shift_hours), key="scenario_shift")

# Check if anything changed
scenario_changed = (
    scenario_machines != 0 or 
    scenario_operators != 0 or 
    scenario_cycle_time != avg_cycle_time or
    scenario_efficiency != operator_efficiency or
    scenario_downtime != downtime_rate or
    scenario_shift != shift_hours
)

if scenario_changed and st.button("🔄 Run Scenario Simulation", key="scenario_btn"):
    with st.spinner("⚡ Running scenario (optimized)..."):
        # Get cached base simulation results with scenario parameters
        scenario_daily_outputs, scenario_weekly_outputs, scenario_downtime_events = run_production_simulation_base(
            num_machines + scenario_machines,
            num_operators + scenario_operators,
            num_simulations, simulation_days,
            scenario_cycle_time, cycle_time_std, scenario_downtime, avg_downtime_duration,
            scenario_efficiency, scenario_shift
        )
        
        scenario_results = calculate_metrics(scenario_daily_outputs, scenario_weekly_outputs, 
                                            scenario_downtime_events, daily_demand, 
                                            num_simulations, simulation_days)
    
    # Comparison Summary
    st.write("---")
    st.write("**📊 Scenario Comparison:**")
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
        roi_text = "✅ Worth it!" if improvement > 5 else "⚠️ Marginal" if improvement > 0 else "❌ No improvement"
        st.metric("ROI Assessment", roi_text)
    
    # Comparison visualization
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
    
    # Build scenario description
    scenario_desc = []
    if scenario_machines != 0:
        scenario_desc.append(f"{scenario_machines:+d} machines")
    if scenario_operators != 0:
        scenario_desc.append(f"{scenario_operators:+d} operators")
    if scenario_cycle_time != avg_cycle_time:
        scenario_desc.append(f"cycle time: {scenario_cycle_time}min")
    if scenario_efficiency != operator_efficiency:
        scenario_desc.append(f"efficiency: {int(scenario_efficiency*100)}%")
    if scenario_downtime != downtime_rate:
        scenario_desc.append(f"downtime: {int(scenario_downtime*100)}%")
    if scenario_shift != shift_hours:
        scenario_desc.append(f"shift: {scenario_shift}h")
    
    scenario_text = " | ".join(scenario_desc) if scenario_desc else "No changes"
    
    fig_compare.update_layout(
        title=f"<b>Daily Output Comparison</b><br><sub>Scenario: {scenario_text}</sub>",
        yaxis_title="Daily Output (units)",
        height=500,
        font=dict(size=11),
        hovermode='y unified'
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)

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
