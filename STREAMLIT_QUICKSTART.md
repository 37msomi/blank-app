# 🚀 Streamlit LMS - Quick Setup Guide

## ⚡ 2-Minute Setup

You already have everything you need!

### Step 1: Install Dependencies
```bash
cd /workspaces/blank-app
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run streamlit_lms_app.py
```

The app opens at: **`http://localhost:8501`**

## 🔓 Login Credentials

Use **any of these** to test different roles:

```
┌─────────────────────────────────┐
│ Employee ID: E001               │
│ Password: password              │
│ Role: Employee                  │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ Employee ID: E002               │
│ Password: password              │
│ Role: Manager                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ Employee ID: E003               │
│ Password: password              │
│ Role: Admin                     │
└─────────────────────────────────┘
```

**All other IDs (E004-E008):** Employee role with password: `password`

## 📊 What Each Role Can Do

### 👤 Employee (E001, E004-E008)
1. **Dashboard** - View your leave balances
2. **New Request** - Submit leave requests
3. See request history with status

### 👔 Manager (E002, E006)
1. **Dashboard** - View your leave balances
2. **New Request** - Submit leave requests  
3. **My Approvals** - Approve/reject pending requests from team

### 🔧 Admin (E003)
1. **Dashboard** - View your leave balances
2. **New Request** - Submit leave requests
3. **Approvals** - Approve/reject any requests
4. **Admin Panel** - See all statistics & reports

## 🎯 Quick Test

### Test 1: Submit a Leave Request
1. Login as **E001** (Employee)
2. Click "📝 New Request"
3. Select "Annual Leave"
4. Pick dates (e.g., 2026-04-01 to 2026-04-05)
5. Add reason and click "✅ Submit Request"
6. ✅ Confirmed! Request appears in Dashboard

### Test 2: Manager Approves Request
1. Logout and login as **E002** (Manager)
2. Click "✅ My Approvals"
3. See Alice Johnson's pending request
4. Click "✅ Approve"
5. ✅ Request status changes to "Approved"

### Test 3: Admin Dashboard
1. Logout and login as **E003** (Admin)
2. Click "🔧 Admin Panel"
3. View:
   - Department statistics
   - Leave utilization metrics
   - All requests overview

## 🎨 UI Features

- **Glassmorphism Design** - Modern frosted glass effect
- **Responsive Layout** - Works on desktop and tablet
- **Dark Sidebar** - Easy on the eyes
- **Status Badges** - Color-coded (Green/Yellow/Red)
- **Smooth Interactions** - Hover effects and animations
- **Real-time Validation** - Form checks as you type

## 📁 Files Overview

```
/workspaces/blank-app/
├── streamlit_lms_app.py      ← Main app (run this!)
├── Employees.csv              ← Employee data
├── LeaveTypes.csv             ← Leave type definitions
├── LeaveRequests.csv          ← Leave request history
├── DepartmentSummary.csv      ← Department stats
├── requirements.txt           ← Python packages
└── LMS_README.md              ← Full documentation
```

## 🛠️ How Relationships Work

### Employee → Manager
```
Employee (E001) has Manager_ID = E002
So E002 can approve E001's requests
```

### Employee → LeaveRequests
```
When E001 submits request, it stores Employee_ID = E001
Then we can fetch all requests where Employee_ID = E001
```

### LeaveRequests → LeaveTypes
```
When viewing requests, we merge with LeaveTypes
to show leave type name instead of just ID
```

## 💾 Data Storage

**All data stored in CSV files:**
- `Employees.csv` - Employee info & balances
- `LeaveRequests.csv` - All submitted requests
- `LeaveTypes.csv` - Leave type definitions
- `DepartmentSummary.csv` - Department stats

**Changes are saved automatically** when you submit forms.

## 🎨 Customization Examples

### Change the primary color
Edit this line in `streamlit_lms_app.py`:
```python
background: linear-gradient(135deg, #6C63FF 0%, #5A57FF 100%);
# Change #6C63FF to your color
```

### Add a new employee
Edit `Employees.csv`, add a row:
```csv
E009,Your Name,email@company.com,Department,Position,employee,MANAGER_ID,20,10,5,0
```

### Add a new leave type
Edit `LeaveTypes.csv`, add a row:
```csv
LT006,Training Leave,5,true,Professional development,#8B5CF6
```

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
# or specifically:
pip install streamlit pandas
```

### "No such file or directory: 'Employees.csv'"
Make sure you're in `/workspaces/blank-app` directory:
```bash
cd /workspaces/blank-app
pwd  # Should show /workspaces/blank-app
```

### App shows blank screen
- Check browser console for errors (F12)
- Restart the app (Ctrl+C, then run again)
- Clear browser cache

### Changes not saving
- CSV files are saved immediately when you submit
- Check if file permissions allow writing
- Restart app to reload data

## 🚀 Deployment

### Run Locally
```bash
streamlit run streamlit_lms_app.py
```

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Streamlit Cloud deploys automatically

### Deploy with Docker
```bash
docker run -p 8501:8501 -v $(pwd):/app streamlit/streamlit-docker streamlit run /app/streamlit_lms_app.py
```

## 📚 Full Documentation

For detailed info, see **`LMS_README.md`**

Topics included:
- ✅ Complete feature list
- ✅ Data model schema
- ✅ UI/UX design details
- ✅ Customization guide
- ✅ Deployment options
- ✅ Future enhancements
- ✅ Code structure reference

## 🎓 Key Concepts

### Streamlit
- Page reruns from top to bottom
- Session state persists across reruns
- `@st.cache_data` speeds up data loading

### Pandas
- `pd.merge()` joins tables (like SQL JOIN)
- `df[df['Column'] == value]` filters data
- `df.to_csv()` saves to file

### CSS Injection
- `st.markdown(css, unsafe_allow_html=True)` adds custom styles
- Glassmorphism uses `backdrop-filter: blur(10px)`
- Custom colors via hex codes `#RRGGBB`

## 💡 Tips

1. **Test all roles** - Login as Employee, Manager, and Admin
2. **Check the data** - Open CSV files in Excel to see relationships
3. **Modify fearlessly** - Changes to CSV reload automatically
4. **Use browser reload** - If UI looks weird, press F5

## 🤝 Need Help?

1. **Read the docstrings** - Code is well-commented
2. **Check function names** - They explain what they do
3. **Review the CSV files** - Data structure is self-explanatory
4. **Read LMS_README.md** - Comprehensive documentation

## ✨ Summary

You now have a **production-ready LMS** with:
- ✅ Pure Python (no JavaScript!)
- ✅ Beautiful Glassmorphism UI
- ✅ Role-based access control
- ✅ Form validation
- ✅ Leave request workflow
- ✅ Manager approvals
- ✅ Admin dashboard
- ✅ CSV data persistence

**Ready to run?**
```bash
streamlit run streamlit_lms_app.py
```

Enjoy! 🎉
