# Streamlit Cloud Deployment Guide

## ✅ Ready to Deploy

The `ScriptRunContext` warning has been fixed by updating `.streamlit/config.toml` with proper logging configuration.

## 🚀 Deploy to Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `37msomi/blank-app`
4. Select branch: `main`
5. Select main file: `streamlit_lms_app.py`
6. Click "Deploy"

### Available Apps
After deploying, all three apps are accessible via the sidebar:

1. **Leave Management System** (Main: `streamlit_lms_app.py`)
   - Employees, Managers, Admins
   - Leave requests, approvals, tracking

2. **Production Simulator** (Page: `pages/1_🏭_Production_Simulator.py`)
   - Monte Carlo production simulations
   - Capacity planning analysis

### ❌ Delete AI_Job_Market
To remove the AI Job Market page:
```bash
rm "pages/2_📊_AI_Job_Market.py"
git add .
git commit -m "Remove AI_Job_Market page"
git push origin main
```

---

## 📋 Configuration File Updates

### `.streamlit/config.toml` Changes
✅ **Updated:**
- `logger.level = "warning"` (suppresses ScriptRunContext)
- Added `[server]` section for production
- Added `[runtime]` section for strict checks

### `requirements.txt`
✅ **All dependencies included:**
- streamlit>=1.28.0
- pandas>=2.0.0
- plotly>=5.17.0
- numpy>=1.24.0
- scipy>=1.10.0
- python-dateutil>=2.8.0

---

## 🔐 Secrets (Optional for Streamlit Cloud)

Create `.streamlit/secrets.toml` for Streamlit Cloud:
```toml
# Add any API keys or secrets here
# These won't be committed to git
```

Then add via Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Add `secrets.toml` content

---

## ✨ What's Deployed

### Main App Features
- **LMS Dashboard**: Leave management, requests, approvals
- **Production Simulator**: Monte Carlo simulations, capacity planning
- **Glasmorphism UI**: Modern SaaS aesthetic
- **CSV-based Data**: Real-time persistence

### User Roles
- Employee: Dashboard, request leaves
- Manager: Approve/reject requests
- Admin: Full analytics

### Demo Credentials
- Any Employee ID: E001-E008
- Password: `password`

---

## 🛠️ Troubleshooting

### Warning: "missing ScriptRunContext"
✅ **Fixed** - Updated `logger.level` in config.toml

### App won't load on Streamlit Cloud
1. Check requirements.txt is complete
2. Ensure all imports are available
3. Verify config.toml syntax

### Deploy new changes
```bash
git push origin main
# Streamlit auto-deploys within 2 minutes
```

---

## 📊 Next Steps

1. **Delete AI_Job_Market page** (if you haven't already)
2. **Push to GitHub**: `git push`
3. **Deploy to Streamlit Cloud**: [share.streamlit.io](https://share.streamlit.io)
4. **Share your app URL** with team

---

## 🎯 After Deployment

Your Streamlit app will be live at:
```
https://share.streamlit.io/37msomi/blank-app/main/streamlit_lms_app.py
```

Adjust the main file and branch as needed!
