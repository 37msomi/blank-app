# 🤖 Data Analytics & Simulation Dashboards

A collection of interactive Streamlit dashboards for data-driven decision making:

1. **🤖 AI Job Impact Dashboard** - Analyze how AI is transforming the global job market
2. **🏭 Production Capacity Simulator** - Optimize manufacturing throughput and plan capacity

---

## 📊 Dashboard 1: AI Job Impact Dashboard (2020–2026)

An interactive data visualization analyzing **AI-driven job market transformation globally**, including automation risk, salary changes, and reskilling urgency across industries and countries.

### Features:
- **Real-time Analytics**: Key metrics on automation risk, AI replacement scores, salary impact, and reskilling urgency
- **Interactive Filters**: Filter by year, industry, and country
- **Multi-dimensional Visualizations**: 
  - Automation risk by industry
  - Salary impact analysis by country
  - Job roles ranked by reskilling urgency
  - Industry trend analysis (2020–2026)
  - Geographic heatmap analysis
- **Detailed Data Export**: View and analyze raw data with a single click

### Run:
```bash
streamlit run streamlit_app.py
```

---

## 🏭 Dashboard 2: Production Throughput & Capacity Planning Simulator

A **Monte Carlo simulation engine** for optimizing factory production capacity, accounting for real-world variability in machine downtime, cycle times, and operator performance.

### Features:
- **Configurable Parameters**:
  - Machine count and operator availability
  - Cycle time variability
  - Machine downtime rates and duration
  - Operator efficiency levels
  - Shift hours and demand targets

- **Monte Carlo Analysis**:
  - 5000+ simulations for statistical significance
  - Daily and weekly output distributions
  - Probability of meeting demand targets
  - Capacity utilization metrics

- **Sensitivity Analysis**:
  - "What-if" scenarios: Add machines/operators
  - Improve operator efficiency
  - ROI assessment for changes
  - Side-by-side comparison vs. baseline

- **Actionable Insights**:
  - Distribution of output with variability quantified
  - Probability of missing demand
  - Whether adding resources actually moves the needle

### Run:
```bash
streamlit run production_simulation.py
```

### Use Cases:
✅ Factory optimization planning
✅ Capacity planning for chocolate production lines
✅ Evaluating if demand can be met under variability
✅ ROI analysis for equipment/staffing investments
✅ Bottleneck identification

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/37msomi/blank-app.git
   cd blank-app
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the desired app
   ```bash
   # AI Job Dashboard
   streamlit run streamlit_app.py
   
   # Production Simulator
   streamlit run production_simulation.py
   ```

4. Open your browser to `http://localhost:8501`

---

## 📁 Project Structure

```
blank-app/
├── streamlit_app.py                          # AI Job Impact Dashboard
├── production_simulation.py                  # Production Capacity Simulator
├── ai_job_replacement_2020_2026_v2.csv       # Job market dataset
├── requirements.txt                          # Python dependencies
└── README.md                                 # This file
```

---

## 📈 Data Overview

### AI Job Market Dataset
- **20+ metrics** from 2020-2026
- **Automation Risk**: % likelihood of job automation
- **AI Replacement Score**: Scale 0-100
- **Salary Impact**: Before/after comparison
- **Reskilling Urgency**: Score indicating skill transition need
- **Geographic Coverage**: Multiple countries, all continents
- **Industry Coverage**: Tech, Finance, Healthcare, Manufacturing, Retail, Education, etc.

### Production Simulation
- **Configurable parameters** for your specific factory
- **Monte Carlo engine** with 5000+ iterations
- **Real-world variability** baked in
- **Probabilistic outputs** for decision making

---

## 🌐 Deploy on Streamlit Cloud

### For AI Dashboard:
1. Push code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app" → Select GitHub repo → Select `streamlit_app.py`
4. Deploy!

### For Production Simulator:
1. Same steps, but select `production_simulation.py`
2. Or deploy both with multi-page app option

**Live access**: Share the generated URL on LinkedIn

---

## 📱 LinkedIn Integration

### Sharing Strategy:

**AI Dashboard Post:**
```
🤖 I analyzed 7 years of job market data showing how AI is reshaping industries.

Key findings:
• Automation risk varies 25-75% by role
• Salary volatility increasing in high-disruption fields
• Tech roles show different trends than manufacturing

Explore the interactive dashboard → [LINK]
```

**Production Simulator Post:**
```
🏭 Built a Monte Carlo simulation to optimize production capacity planning.

Using real-world variability:
• Machine downtime
• Cycle time fluctuations  
• Operator performance variability

Results show if adding resources actually moves the needle. Check it out → [LINK]
```

---

## 🛠️ Technologies Used

- **Streamlit**: Interactive web app framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations
- **SciPy**: Statistical functions
- **Monte Carlo Simulation**: Probabilistic analysis

---

## 💡 Use Cases

### AI Job Impact Dashboard
- 📌 **Recruitment Teams**: Identify critical skills and affected roles
- 📌 **HR Professionals**: Plan reskilling and career development
- 📌 **Policy Makers**: Understand labor market trends
- 📌 **Job Seekers**: Assess automation risk in your field
- 📌 **Analysts**: Deep-dive into global job transformation

### Production Simulator
- 📌 **Factory Managers**: Optimize production scheduling
- 📌 **Operations Teams**: Identify capacity bottlenecks
- 📌 **CFOs**: Evaluate ROI of equipment investments
- 📌 **Quality Teams**: Plan for variability in output
- 📌 **Supply Chain**: Forecast realistic delivery windows

---

## 📧 Contact & LinkedIn

**Portfolio**: [View on LinkedIn](https://www.linkedin.com/in/yourprofile)

Feel free to fork, modify, and deploy these dashboards!

---

**License**: MIT License (See LICENSE file)
