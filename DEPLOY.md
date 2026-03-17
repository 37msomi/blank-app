# 🚀 Streamlit Cloud Deployment Guide

## Quick Summary

You now have a **multi-page Streamlit app** ready for deployment:
- **Main entry point**: `app.py`
- **Pages**: `pages/1_🏭_Production_Simulator.py` and `pages/2_📊_AI_Job_Market.py`
- **Config**: `.streamlit/config.toml`
- **Dependencies**: `requirements.txt` (already up to date)

---

## Step 1: Push Code to GitHub

```bash
# Initialize (if not already done)
git init
git add .
git commit -m "Multi-page Streamlit app with Production Simulator"
git remote add origin https://github.com/YOUR_USERNAME/blank-app.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Streamlit Cloud

### Option A: Deploy Production Simulator Only (Single Page)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select **GitHub repo**: `37msomi/blank-app`
4. **Branch**: `main`
5. **File path**: `production_simulation.py`  ← Select this for single-page app
6. Click **Deploy**

**Result**: Your app will be live at: `https://share.streamlit.io/37msomi/blank-app/main/production_simulation.py`

---

### Option B: Deploy Multi-Page App (Both Dashboards)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select **GitHub repo**: `37msomi/blank-app`
4. **Branch**: `main`
5. **File path**: `app.py`  ← Select this for multi-page app
6. Click **Deploy**

**Result**: Your app will be live at: `https://share.streamlit.io/37msomi/blank-app/main/app.py`

Users will see a sidebar menu with both dashboards automatically!

---

## Step 3: Configure Secrets (Optional)

If your app needs API keys or database credentials:

1. Go to your app's settings on Streamlit Cloud
2. Click **"Secrets"**
3. Add your secrets in TOML format:
   ```toml
   database_url = "postgresql://..."
   api_key = "sk-..."
   ```

Access them in code with:
```python
import streamlit as st
db_url = st.secrets["database_url"]
```

---

## Step 4: Share on LinkedIn

### Production Simulator Post:

```
🏭 I built a Monte Carlo simulator for production capacity planning.

With real-world variability (machine downtime, cycle times, operator performance), 
this helps optimize factory throughput and meet demand targets.

Key features:
• 5000+ simulations for statistical accuracy
• "What-if" scenario analysis (ROI of adding machines/operators)
• Probability of meeting demand targets
• Cumulative probability analysis

Check it out: [YOUR_STREAMLIT_URL]

#Manufacturing #OperationsResearch #DataScience #MonteCarlo
```

### Multi-App Post:

```
📊 I built a production analytics platform with two dashboards:

1. 🏭 Production Capacity Simulator - Optimize factory throughput
2. 📈 AI Job Market Impact - Analyze global job transformation

Both use interactive visualizations and Monte Carlo simulations to deliver 
actionable insights for decision-makers.

Explore here: [YOUR_STREAMLIT_URL]

#DataDriven #Analytics #OperationsResearch #LinkedIn
```

---

## Troubleshooting

### App Won't Deploy
- **Check**: requirements.txt has all dependencies
- **Fix**: Make sure pandas, plotly, numpy, scipy are listed

### Missing Data File
- **Issue**: `ai_job_replacement_2020_2026_v2.csv` not found
- **Fix**: Ensure CSV is in repository root and committed to GitHub
  ```bash
  git add ai_job_replacement_2020_2026_v2.csv
  git commit -m "Add job market dataset"
  git push
  ```

### Slow Performance
- **Cause**: Streamlit Cloud runs on limited resources
- **Fix**: The production simulator uses `@st.cache_data` for optimization
- **Note**: First load may take 10-15 seconds, subsequent loads are instant

### Secrets Not Loading
- **Issue**: `st.secrets` returns error
- **Fix**: Go to app settings → Secrets and ensure TOML is valid

---

## Monitoring & Logs

After deployment:

1. Go to your app settings on Streamlit Cloud
2. Click **"Logs"** to see real-time execution logs
3. Check for errors in red text

---

## Next Steps

- ✅ App deployed and public
- 📱 Share on LinkedIn with the post templates above
- 🔄 Update & redeploy: Just push new code to GitHub, Streamlit auto-deploys!
- 📊 Track analytics: See how many people use your dashboards in the Streamlit Cloud dashboard

---

## Optional: Custom Domain

Want a custom URL like `production-simulator.com`?

1. In Streamlit Cloud settings, go to **"Custom domain"**
2. Point your domain to Streamlit using the provided DNS settings
3. Streamlit Cloud handles SSL/HTTPS automatically

---

**Your app is now ready to showcase your analytics expertise!** 🎯

Questions? Check [Streamlit Cloud docs](https://docs.streamlit.io/streamlit-cloud)
