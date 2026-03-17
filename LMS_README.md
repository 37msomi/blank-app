# Leave Management System (LMS) - Streamlit Version

## 🎯 Overview

A **Python-only Leave Management System** built with Streamlit featuring:
- ✅ SaaS-style dashboard with **Glassmorphism** styling
- ✅ Role-based views (Employee, Manager, Admin)
- ✅ Leave request submission with validation
- ✅ Manager approval workflow
- ✅ Admin statistics dashboard
- ✅ Data persistence via CSV files
- ✅ Clean, modern UI with custom CSS

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /workspaces/blank-app
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run streamlit_lms_app.py
```

The app will open at `http://localhost:8501`

### 3. Login with Demo Credentials
- **Employee ID:** E001 (any from E001 to E008)
- **Password:** `password`

## 📊 Features by Role

### 👤 **Employee View**
- **Dashboard:** View remaining leave balance (Annual, Sick, Personal)
- **Leave Request History:** See all your submitted requests with status
- **Submit Request:** New leave request form with:
  - Leave type selection
  - Date range picker
  - Reason textarea
  - Automatic validation (balance check, max days check)

### 👔 **Manager View**
- All Employee features PLUS
- **My Approvals:** View pending requests from managed employees
- **Approve/Reject:** Inline approval with optional rejection reason
- **Request Details:** Employee info, dates, and reason visibility

### 🔧 **Admin View**
- All Employee & Manager features PLUS
- **Admin Dashboard:** 
  - Department statistics
  - Leave utilization metrics
  - All requests overview
  - Pending requests count

## 🗂️ File Structure

```
/workspaces/blank-app/
├── streamlit_lms_app.py          ← Main Streamlit app
├── Employees.csv                 ← Employee data
├── LeaveTypes.csv                ← Leave type definitions
├── LeaveRequests.csv             ← Leave request history
├── DepartmentSummary.csv         ← Department statistics
├── requirements.txt              ← Python dependencies
└── README.md                     ← This file
```

## 📋 Data Model

### Employees.csv
| Column | Type | Description |
|--------|------|-------------|
| Employee_ID | string | Unique ID (E001, E002, etc.) |
| Name | string | Employee name |
| Email | string | Company email |
| Department | string | Department name |
| Position | string | Job title |
| Role | string | employee, manager, or admin |
| Manager_ID | string | Reports to (FK) |
| Annual_Leave_Balance | int | Days available |
| Sick_Leave_Balance | int | Days available |
| Personal_Leave_Balance | int | Days available |
| Total_Days_Used | int | Days used this period |

### LeaveTypes.csv
| Column | Type | Description |
|--------|------|-------------|
| LeaveType_ID | string | Unique ID (LT001, etc.) |
| Name | string | Leave type name |
| Max_Days | int | Maximum days allowed |
| Requires_Approval | bool | Needs approval |
| Description | string | Leave details |
| Color | string | Hex color for UI |

### LeaveRequests.csv
| Column | Type | Description |
|--------|------|-------------|
| Request_ID | string | Unique ID |
| Employee_ID | string | FK to Employees |
| LeaveType_ID | string | FK to LeaveTypes |
| Start_Date | date | Leave start |
| End_Date | date | Leave end |
| Reason | string | Reason for leave |
| Status | string | pending, approved, rejected |
| Approver_ID | string | Manager who approved |
| Days_Requested | int | Total days |
| Submission_Date | date | When submitted |
| Approval_Date | date | When approved |
| Rejection_Reason | string | If rejected |

### DepartmentSummary.csv
| Column | Type | Description |
|--------|------|-------------|
| Department | string | Department name |
| Total_Employees | int | Employee count |
| Pending_Requests | int | Pending approvals |
| Approved_Requests | int | Approved this period |
| Total_Leave_Days_Used | int | Days used |
| Annual_Leave_Pool | int | Total available |
| Annual_Leave_Used | int | Days used |

## 🎨 UI/UX Design

### Glassmorphism Style
- **Backdrop Blur:** Semi-transparent cards with blur effect
- **Gradient Backgrounds:** Subtle color gradients
- **Soft Shadows:** Layered shadow effects for depth
- **Rounded Cards:** 16px border radius on containers
- **Color Scheme:**
  - Primary: `#6C63FF` (Purple)
  - Background: `#F0F2F6` (Light gray)
  - Sidebar: `#1F2937` (Dark gray)
  - Success: `#10B981` (Green)
  - Warning: `#F59E0B` (Orange)
  - Error: `#EF4444` (Red)

### Components
- **Metric Cards:** Leave balance display with hover effects
- **Status Badges:** Color-coded status indicators
- **Form Inputs:** Custom styled with focus states
- **Tables:** Responsive dataframes with custom styling
- **Buttons:** Gradient buttons with shadow effects

## 🔐 Authentication

### Simple Auth (Demo)
- Employee ID + Password (default: "password")
- No external authentication service
- Session state management with Streamlit

### Production Considerations
- Implement proper password hashing
- Add LDAP/SSO integration
- Store credentials securely
- Add multi-factor authentication

## 💾 Data Persistence

### CSV-Based Storage
- All data stored in CSV files
- Automatic reloading when files change
- Changes saved immediately to CSV

### Advantages
- ✅ No database setup required
- ✅ Easy to backup/version control
- ✅ Simple to understand and modify
- ✅ Perfect for small to medium teams

### Limitations
- ❌ No concurrent write protection
- ❌ Limited query capability
- ❌ Not suitable for large datasets

### Production Migration
For production, consider migrating to:
- PostgreSQL
- MongoDB
- Firebase/Firestore
- SQLAlchemy ORM

## 🧪 Testing the System

### Test 1: Employee Request Submission
1. Login as **E004** (employee)
2. Go to "New Request"
3. Select "Annual Leave"
4. Pick dates (within balance)
5. Add reason and submit
6. Verify request appears in "Dashboard"

### Test 2: Manager Approval
1. Note request ID from Test 1
2. Logout and login as **E002** (manager)
3. Go to "My Approvals"
4. See pending request from E004
5. Click "Approve"
6. Verify status changes to "approved"

### Test 3: Admin View
1. Login as **E003** (admin)
2. Go to "Admin Panel"
3. See department statistics
4. Verify all requests count

## 🛠️ Customization Guide

### Add New Leave Type
1. Open `LeaveTypes.csv`
2. Add new row with unique LeaveType_ID
3. Restart the app

### Add New Employee
1. Open `Employees.csv`
2. Add row with Employee_ID, Name, Role, etc.
3. Set initial leave balances
4. Assign manager via Manager_ID

### Change Colors
Edit the CSS in `streamlit_lms_app.py` function `inject_css()`:
```python
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Modify Validation Rules
Edit the validation logic in `show_leave_request_form()`:
```python
if days_requested > max_days:
    # Custom validation
```

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_lms_app.py
```

### Streamlit Cloud
1. Push repo to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Self-Hosted (Docker)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_lms_app.py"]
```

## 📈 Future Enhancements

- [ ] Email notifications for approvals
- [ ] Calendar visualization
- [ ] Export to PDF/Excel
- [ ] Recurring leave patterns
- [ ] Team leave view
- [ ] Advanced analytics
- [ ] Approval workflow customization
- [ ] Mobile-responsive improvements
- [ ] Real-time notifications
- [ ] Database backend (PostgreSQL)

## ⚠️ Limitations & Fixes

### Issue: Session state resets on page refresh
**Solution:** Streamlit reloads the entire script. Use `@st.cache_data` for data loading.

### Issue: Data not persisting
**Solution:** Manually save DataFrames to CSV with `df.to_csv()`

### Issue: Multiple approvals at once
**Solution:** Add timestamp check to prevent duplicate approvals

### Issue: Password security
**Solution:** Switch to proper auth system (Firebase, Auth0, etc.)

## 📚 Code Structure

### Key Functions

#### `inject_css()`
Inserts custom CSS for Glassmorphism styling

#### `load_employees()` / `load_leave_types()` / etc.
Cached data loaders for CSV files

#### `authenticate(employee_id, password)`
Validates credentials and sets session state

#### `get_user_leave_balance(employee_id)`
Calculates remaining leave for employee

#### `show_employee_dashboard()`
Renders employee view with metrics

#### `show_leave_request_form()`
Form with validation for new requests

#### `show_manager_approvals()`
Displays pending requests for manager approval

#### `show_admin_dashboard()`
Admin statistics and overview

## 🔗 Integration Points

### CSV Data
```python
employees_df = pd.read_csv('Employees.csv')
leave_requests_df = pd.read_csv('LeaveRequests.csv')
```

### Pandas Merges (Relationships)
```python
requests.merge(employees_df, left_on='Employee_ID', right_on='Employee_ID')
```

### Session State
```python
st.session_state.current_user = {...}
st.session_state.is_authenticated = True
```

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Glassmorphism UI](https://css-tricks.com/glassmorphism/)
- [CSS Grid & Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

## 📞 Support

For issues or questions:
1. Check the Streamlit documentation
2. Review the code comments in `streamlit_lms_app.py`
3. Examine the CSV structure
4. Test with demo credentials

## 📝 License

MIT - Use freely for personal or commercial projects
