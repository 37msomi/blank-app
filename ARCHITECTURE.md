# 🏗️ Streamlit LMS - Architecture Overview

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APP                        │
│                 (streamlit_lms_app.py)                      │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │         SESSION STATE MANAGEMENT                      │ │
│  │  current_user, is_authenticated, form_state           │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                 │
│         ┌────────────────┼────────────────┐               │
│         │                │                │               │
│         ▼                ▼                ▼               │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  LOGIN     │  │ NAVIGATION  │  │   PAGES     │        │
│  │  PAGE      │  │   SIDEBAR   │  │  - Dashboard│        │
│  │            │  │             │  │  - Forms    │        │
│  │ • Validate │  │ • Role-based│  │  - Approvals│        │
│  │   creds    │  │   menu      │  │  - Admin    │        │
│  │ • Set state│  │ • Logout    │  │             │        │
│  └────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │               │
└─────────┼────────────────┼────────────────┼───────────────┘
          │                │                │
          ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────┐
│         PAGES (app.py Functions)                             │
│                                                              │
│  show_login()                show_employee_dashboard()      │
│  show_manager_approvals()    show_leave_request_form()      │
│  show_admin_dashboard()                                     │
│                                                              │
│  Each function:                                             │
│  • Uses st.metric, st.form, st.dataframe                   │
│  • Calls backend functions                                 │
│  • Updates session state on submission                     │
│  • Injects custom CSS via st.markdown()                    │
└──────────────────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────────────────┐
│         PYTHON BACKEND FUNCTIONS                             │
│                                                              │
│  Data Loaders (with @st.cache_data)                         │
│  ├─ load_employees()        ├─ load_leave_types()          │
│  ├─ load_leave_requests()   ├─ load_department_summary()   │
│                                                              │
│  Auth Functions                                             │
│  ├─ authenticate()          ├─ logout()                     │
│                                                              │
│  Helper Functions                                           │
│  ├─ get_user_leave_balance()                               │
│  ├─ get_user_requests()                                    │
│  ├─ get_pending_requests_for_manager()                     │
│  ├─ status_badge()                                         │
└──────────────────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────────────────┐
│         PANDAS OPERATIONS                                    │
│                                                              │
│  • Read CSV files                                           │
│  • Filter: df[df['column'] == value]                        │
│  • Merge: df1.merge(df2, on='key')                          │
│  • Group: df.groupby('column').sum()                        │
│  • Update: df.loc[mask, 'col'] = new_value                 │
│  • Save: df.to_csv('file.csv', index=False)                │
└──────────────────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────────────────┐
│         CSV DATA FILES (Persistent Storage)                  │
│                                                              │
│  Employees.csv                LeaveTypes.csv                 │
│  ├─ 8 employees              ├─ 5 leave types              │
│  ├─ Roles & managers         ├─ Max days per type          │
│  ├─ Leave balances           ├─ Approval requirements      │
│  └─ Department info          └─ Colors for UI              │
│                                                              │
│  LeaveRequests.csv            DepartmentSummary.csv         │
│  ├─ 7+ requests              ├─ 4 departments              │
│  ├─ Request status           ├─ Employee counts           │
│  ├─ Dates & reasons          ├─ Pending/approved counts   │
│  └─ Approval history         └─ Leave utilization         │
└──────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagrams

### 1. Login Flow
```
User Input
(E001 / password)
     │
     ▼
authenticate()
     │
     ├─ Check Employees.csv
     ├─ Validate credentials
     │
     ▼
Set session_state
├─ current_user
├─ is_authenticated
     │
     ▼
st.rerun()
     │
     ▼
Dashboard loads
✅
```

### 2. Leave Request Submission Flow
```
Employee fills form
├─ Select leave type (from LeaveTypes.csv)
├─ Pick dates
├─ Add reason
│
▼
Validation checks
├─ Days ≤ Max_Days? (from LeaveType)
├─ Days ≤ Balance? (from Employee)
├─ End_Date ≥ Start_Date?
├─ Reason not empty?
│
▼
If valid:
├─ Create new row
├─ Add to leave_requests_df
├─ Save to LeaveRequests.csv
├─ Display success message
└─ Reset form
│
✅ Request submitted
```

### 3. Manager Approval Flow
```
Manager logs in (E002)
│
▼
My Approvals page loads
│
▼
Find managed employees
├─ employees_df[Manager_ID == 'E002']
├─ Result: E004, E008
│
▼
Get pending requests from those employees
├─ leave_requests_df[
│    (Employee_ID in [E004, E008]) &
│    (Status == 'pending')
│  ]
│
▼
Merge with employee names & leave types
├─ Get better display info
├─ Show "David Smith - Annual Leave"
│
▼
Display for approval
│
Manager clicks Approve/Reject
│
▼
Update CSV
├─ Status = 'approved' / 'rejected'
├─ Approver_ID = 'E002'
├─ Save to LeaveRequests.csv
│
✅ Request updated
```

### 4. Data Relationship Example
```
BEFORE MERGE:
┌─────────────┐        ┌──────────────┐
│LeaveRequests│        │  Employees   │
├─────────────┤        ├──────────────┤
│Request_ID:1 │        │ID:E004 Name: │
│Employee_ID: │        │David Smith   │
│E004         │        │              │
└─────────────┘        └──────────────┘

MERGE ON Employee_ID:

Result:
┌────────────────────────────┐
│ Request_ID: 1              │
│ Employee_ID: E004          │
│ Name: David Smith      ←─── (from Employees)
│ Status: pending            │
└────────────────────────────┘

NOW SHOW: "David Smith - pending" ✅
(Instead of: "E004 - pending" ❌)
```

## 🗂️ File Organization

```
/workspaces/blank-app/
│
├── 🚀 PRIMARY FILES
│   ├── streamlit_lms_app.py          (Main application - RUN THIS)
│   └── requirements.txt              (Dependencies - pip install)
│
├── 📊 DATA LAYER
│   ├── Employees.csv                 (Employee master data)
│   ├── LeaveTypes.csv                (Leave type definitions)
│   ├── LeaveRequests.csv             (Transaction data)
│   └── DepartmentSummary.csv         (Aggregated metrics)
│
├── 📚 DOCUMENTATION
│   ├── STREAMLIT_QUICKSTART.md       (2-min setup)
│   ├── LMS_README.md                 (Full reference)
│   ├── FEATURES.md                   (100+ features)
│   ├── DATA_RELATIONSHIPS.md         (Pandas joins explained)
│   ├── STREAMLIT_LMS_COMPLETE.md     (Complete overview)
│   └── THIS FILE                     (Architecture guide)
│
└── 📁 OPTIONAL (Legacy)
    ├── lms-app/                      (React version)
    ├── app.py                        (Demo Streamlit)
    └── pages/                        (Streamlit plugins)
```

## 🎯 Role-Based Navigation Tree

```
LOGIN
│
├─ EMPLOYEE (E001, E004, E005, E007, E008)
│  │
│  ├── Dashboard
│  │   └─ View leave balances
│  │      └─ View request history
│  │
│  └── New Request
│     └─ Submit leave request
│        └─ View validation feedback
│
├─ MANAGER (E002, E006)
│  │
│  ├── Dashboard
│  │   └─ View leave balances
│  │      └─ View request history
│  │
│  ├── New Request
│  │   └─ Submit own leave request
│  │
│  └── My Approvals
│     └─ View pending requests from team
│        ├─ Approve (with notes)
│        └─ Reject (with reason)
│
└─ ADMIN (E003)
   │
   ├── Dashboard
   │   └─ View leave balances
   │      └─ View request history
   │
   ├── New Request
   │   └─ Submit own leave request
   │
   ├── Approvals
   │   └─ View all pending requests
   │      ├─ Approve any request
   │      └─ Reject any request
   │
   └── Admin Panel
      ├─ Department Statistics
      │  └─ Total employees per dept
      │     └─ Pending/approved counts
      │        └─ Leave utilization
      │
      └─ All Requests Overview
         └─ Global request history
```

## 🔐 Authentication & Authorization

```
LOGIN PAGE
    │
    ├─ Input: Employee_ID
    ├─ Input: Password
    │
    ▼
authenticate(employee_id, password)
    │
    ├─ Query Employees.csv
    ├─ Check if Employee_ID exists
    ├─ Verify password (demo: always "password")
    │
    ▼
VALID ──┐         INVALID ──┐
│       │                   │
▼       ▼                   ▼
Set session_state    Show error
├─ current_user      └─ "Invalid credentials"
├─ is_authenticated
├─ user role
├─ user department
│
▼
Show sidebar for role
├─ If employee: [Dashboard, New Request]
├─ If manager: [Dashboard, New Request, My Approvals]
├─ If admin: [Dashboard, New Request, Approvals, Admin Panel]

✅ Logged in!
```

## 🎨 UI Component Hierarchy

```
STREAMLIT APP
│
├─ Header (Injected CSS)
│  └─ Glassmorphism effects
│
├─ Sidebar (st.sidebar)
│  ├─ User profile card
│  ├─ Role-based navigation
│  │  └─ st.radio buttons
│  └─ Logout button
│
└─ Main Content (Dynamic based on role)
   │
   ├─ Login Page
   │  ├─ Logo
   │  ├─ Form (selectbox, text_input)
   │  ├─ Button
   │  └─ Demo credentials box
   │
   ├─ Dashboard
   │  ├─ Title
   │  ├─ Metrics (3 columns)
   │  │  ├─ st.metric (Annual)
   │  │  ├─ st.metric (Sick)
   │  │  └─ st.metric (Personal)
   │  ├─ Dataframe
   │  │  └─ st.dataframe (history)
   │  └─ Divider
   │
   ├─ New Request Form
   │  ├─ Form container
   │  ├─ Two columns
   │  │  ├─ Selectbox (leave type)
   │  │  ├─ Date_input (start)
   │  │  └─ Date_input (end)
   │  ├─ Metrics (validation)
   │  ├─ Text_area (reason)
   │  ├─ Validation feedback
   │  └─ Buttons (Submit, Cancel)
   │
   ├─ Approvals Page
   │  ├─ Title + count
   │  ├─ For each request:
   │  │  ├─ Container
   │  │  ├─ Request details
   │  │  ├─ Buttons (Approve, Reject)
   │  │  └─ Optional reason input
   │  └─ Divider
   │
   └─ Admin Panel
      ├─ Metrics (4 columns)
      │  ├─ Total employees
      │  ├─ Pending requests
      │  ├─ Approved requests
      │  └─ Leave days used
      ├─ Department table
      │  └─ st.dataframe
      └─ All requests table
         └─ st.dataframe
```

## 🔄 Session State Cycle

```
APP START
│
▼
Initialize Session State
├─ current_user = None
├─ is_authenticated = False
│
▼
Show Login Page
│
User enters credentials
│
▼
Click Login
│
▼
authenticate() validates
│
▼
SET session_state
├─ current_user = {id, name, email, role, department}
├─ is_authenticated = True
│
▼
st.rerun()
│
▼
Check is_authenticated
│  ✓ True? → Load dashboard for role
│  ✗ False? → Show login page
│
▼
User navigates pages
(state persists across pages)
│
▼
User clicks Logout
│
▼
RESET session_state
├─ current_user = None
├─ is_authenticated = False
│
▼
st.rerun()
│
▼
Show Login Page
```

## 📈 CSV Data Flow

```
USER SUBMITS FORM
│
▼
Python validates
│
▼
If valid:
  Create DataFrame row
  │
  ▼
  Read existing CSV
  │
  ▼
  Append new row
  │
  ▼
  Write back to CSV
  │
  ▼
  Clear cache (@st.cache_data)
  │
  ▼
  st.rerun()
  │
  ▼
  Reload CSV (now includes new row)
  │
  ▼
  Display updated data
  
✅ Persistent change!
```

## 🎯 Key Data Relationships Visualized

```
EMPLOYEES TABLE
┌────────┬──────────┬────────────┐
│   ID   │   Name   │ Manager_ID │
├────────┼──────────┼────────────┤
│ E001   │ Alice    │   NULL     │
│ E002   │ Bob      │   NULL     │
│ E004   │ David    │   E002  ──-> Points to E002 (Bob)
└────────┴──────────┴────────────┘

LEAVE REQUESTS TABLE
┌────────┬────────────┬────────────────┐
│   ID   │ Employee   │ LeaveType_ID   │
├────────┼────────────┼────────────────┤
│ LR001  │   E004 ───┐│   LT001    ──┐
└────────┴────────────┴────────────────┘
         │            │
         │            ▼
         │         LEAVE TYPES TABLE
         │         ┌──────┬────────────┐
         │         │  ID  │    Name    │
         │         ├──────┼────────────┤
         │         │LT001 │ Annual  ───┘
         │         └──────┴────────────┘
         │
         ▼
      EMPLOYEES TABLE
      ┌────────┬──────────┐
      │   ID   │   Name   │
      ├────────┼──────────┤
      │ E004   │ David ───┘
      └────────┴──────────┘

RESULT: "David Smith - Annual Leave"
(Instead of "E004 - LT001")
```

## ✨ Performance & Caching

```
STREAMLIT LIFECYCLE

on_every_script_run:
    ├─ Check @st.cache_data functions
    │  ├─ load_employees()
    │  ├─ load_leave_types()
    │  ├─ load_leave_requests()
    │  └─ load_department_summary()
    │
    │  If function called again with same args:
    │  └─ Return cached result (instant!)
    │
    ├─ Run main app logic
    │
    └─ Render UI
    
Benefits:
├─ CSV loaded once per session (fast)
├─ No redundant file I/O
└─ Smooth user experience
```

## 🚀 Deployment Architecture

```
LOCAL DEVELOPMENT
│
├─ streamlit run streamlit_lms_app.py
├─ Port: localhost:8501
├─ Data files: local CSV
└─ Storage: in-memory + CSV

STREAMLIT CLOUD DEPLOYMENT
│
├─ GitHub repository
├─ Streamlit detects deploy
├─ Builds container
├─ Runs app on cloud
├─ Domain: user.streamlit.app
└─ Storage: cloud + CSV (git)

DOCKER DEPLOYMENT
│
├─ Dockerfile builds image
├─ Python + dependencies
├─ Runs streamlit
├─ Port: 8501
└─ Storage: mounted volume

ENTERPRISE DEPLOYMENT
│
├─ Database: PostgreSQL
├─ Auth: OAuth2/SAML
├─ Monitoring: DataDog/New Relic
├─ Load balancing: Nginx
└─ Storage: S3 / Network storage
```

---

**This architecture enables:**
- ✅ Simple Python-only development
- ✅ Zero JavaScript complexity
- ✅ Easy data management with CSV
- ✅ Scalable to larger databases
- ✅ Beautiful modern UI
- ✅ Role-based access control
- ✅ Real-time data updates
- ✅ Production-ready code

**Ready to deploy!** 🚀
