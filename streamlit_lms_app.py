import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="Leave Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# GLASSMORPHISM CSS STYLING
def inject_css():
    css = """
    <style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #F0F2F6 0%, #E8EAEF 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1F2937 0%, #111827 100%);
    }
    
    /* Metric cards - Glassmorphism effect */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        background: rgba(255, 255, 255, 0.98);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
        transform: translateY(-4px);
    }
    
    /* Cards container */
    .card-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(211, 213, 219, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 
                    0 10px 13px rgba(0, 0, 0, 0.06);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #5A57FF 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5A57FF 0%, #4A4EFF 100%);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Dataframe */
    [data-testid="dataframe"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Status badges */
    .status-approved {
        background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
        color: #065F46;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #FEF3C7, #FCD34D);
        color: #92400E;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .status-rejected {
        background: linear-gradient(135deg, #FEE2E2, #FCA5A5);
        color: #7F1D1D;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    /* Forms */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #E5E7EB;
        border-radius: 12px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #6C63FF;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1);
    }
    
    /* Sidebar text colors */
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1F2937;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 12px !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_css()

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
@st.cache_data
def load_employees():
    return pd.read_csv('Employees.csv')

@st.cache_data
def load_leave_types():
    return pd.read_csv('LeaveTypes.csv')

@st.cache_data
def load_leave_requests():
    return pd.read_csv('LeaveRequests.csv')

@st.cache_data
def load_department_summary():
    return pd.read_csv('DepartmentSummary.csv')

# Load data
employees_df = load_employees()
leave_types_df = load_leave_types()
leave_requests_df = load_leave_requests()
department_df = load_department_summary()

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================
def authenticate(employee_id, password):
    """Simple authentication - in production, use secure methods"""
    # Demo: Accept any employee ID with 'password' as password
    if employee_id in employees_df['Employee_ID'].values and password == 'password':
        user = employees_df[employees_df['Employee_ID'] == employee_id].iloc[0]
        st.session_state.current_user = {
            'id': user['Employee_ID'],
            'name': user['Name'],
            'email': user['Email'],
            'role': user['Role'],
            'department': user['Department'],
        }
        st.session_state.is_authenticated = True
        return True
    return False

def logout():
    st.session_state.current_user = None
    st.session_state.is_authenticated = False

# ============================================================================
# LOGIN PAGE
# ============================================================================
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="card-container" style="text-align: center; padding: 40px;">
        <h1 style="margin-bottom: 10px; color: #6C63FF;">🏢 LMS</h1>
        <h3>Leave Management System</h3>
        <p style="color: #6B7280; margin-top: 20px;">Sign in to manage your leave requests</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            employee_id = st.selectbox(
                "Employee ID",
                sorted(employees_df['Employee_ID'].values),
                help="Select your employee ID"
            )
            password = st.text_input("Password", type="password", help="Enter 'password' for demo")
            
            if st.form_submit_button("🔓 Login", use_container_width=True):
                if authenticate(employee_id, password):
                    st.success(f"Welcome, {st.session_state.current_user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. (Hint: password is 'password')")
        
        st.markdown("""
        ---
        **Demo Credentials:**
        - Employee IDs: E001, E002, E003...
        - Password: `password` (for all)
        
        **Roles:**
        - 👤 **Employee** (E001, E004, E005, E007, E008)
        - 👔 **Manager** (E002, E006)
        - 🔧 **Admin** (E003)
        """)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_user_leave_balance(employee_id):
    """Get current leave balance for an employee"""
    employee = employees_df[employees_df['Employee_ID'] == employee_id].iloc[0]
    return {
        'annual': employee['Annual_Leave_Balance'],
        'sick': employee['Sick_Leave_Balance'],
        'personal': employee['Personal_Leave_Balance'],
    }

def get_user_requests(employee_id):
    """Get all leave requests for an employee"""
    requests = leave_requests_df[leave_requests_df['Employee_ID'] == employee_id].copy()
    return requests.merge(leave_types_df[['LeaveType_ID', 'Name', 'Color']], 
                          left_on='LeaveType_ID', right_on='LeaveType_ID')

def get_pending_requests_for_manager(manager_id):
    """Get all pending requests for a manager to approve"""
    # Get employees managed by this manager
    managed_employees = employees_df[employees_df['Manager_ID'] == manager_id]['Employee_ID'].values
    
    # Get pending requests from managed employees
    pending = leave_requests_df[
        (leave_requests_df['Employee_ID'].isin(managed_employees)) & 
        (leave_requests_df['Status'] == 'pending')
    ].copy()
    
    # Add employee names
    pending = pending.merge(employees_df[['Employee_ID', 'Name', 'Email', 'Department']], 
                           left_on='Employee_ID', right_on='Employee_ID')
    # Add leave type names
    pending = pending.merge(leave_types_df[['LeaveType_ID', 'Name']], 
                           left_on='LeaveType_ID', right_on='LeaveType_ID', 
                           suffixes=('', '_LeaveType'))
    
    return pending

def status_badge(status):
    """Create HTML badge for status"""
    if status == 'approved':
        return '<span class="status-approved">✓ Approved</span>'
    elif status == 'pending':
        return '<span class="status-pending">⏳ Pending</span>'
    elif status == 'rejected':
        return '<span class="status-rejected">✗ Rejected</span>'
    return status

# ============================================================================
# DASHBOARD - EMPLOYEE VIEW
# ============================================================================
def show_employee_dashboard():
    st.title("📊 Dashboard")
    
    user_id = st.session_state.current_user['id']
    balance = get_user_leave_balance(user_id)
    
    # Leave Balance Metrics
    st.subheader("Your Leave Balance")
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.metric("Annual Leave", f"{balance['annual']} days", "Primary leave entitlement")
    with col2:
        st.metric("Sick Leave", f"{balance['sick']} days", "Medical leave")
    with col3:
        st.metric("Personal Leave", f"{balance['personal']} days", "Personal reasons")
    
    # Leave Request History
    st.subheader("Your Leave Request History")
    requests = get_user_requests(user_id)
    
    if len(requests) > 0:
        # Create display dataframe
        display_df = requests[[
            'Request_ID', 'Name', 'Start_Date', 'End_Date', 
            'Days_Requested', 'Status', 'Reason'
        ]].copy()
        display_df.columns = ['Request ID', 'Leave Type', 'Start Date', 'End Date', 
                             'Days', 'Status', 'Reason']
        
        # Color code status
        def color_status(s):
            if s == 'approved':
                return '🟢 Approved'
            elif s == 'pending':
                return '🟡 Pending'
            elif s == 'rejected':
                return '🔴 Rejected'
            return s
        
        display_df['Status'] = display_df['Status'].apply(color_status)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No leave requests yet. Submit your first request below!")

# ============================================================================
# LEAVE REQUEST FORM
# ============================================================================
def show_leave_request_form():
    st.title("📝 Submit Leave Request")
    
    user_id = st.session_state.current_user['id']
    balance = get_user_leave_balance(user_id)
    
    st.markdown("""
    <div class="card-container">
    <h3 style="color: #1F2937; margin-top: 0;">New Leave Request</h3>
    <p style="color: #6B7280;">Submit a formal request for leave. Requests requiring approval will be reviewed by your manager.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("leave_request_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            leave_type = st.selectbox(
                "Leave Type",
                leave_types_df['Name'].values,
                help="Select the type of leave"
            )
            selected_type = leave_types_df[leave_types_df['Name'] == leave_type].iloc[0]
            max_days = selected_type['Max_Days']
            
            start_date = st.date_input(
                "Start Date",
                value=datetime.now(),
                min_value=datetime.now()
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now() + timedelta(days=1),
                min_value=datetime.now()
            )
            
            days_requested = (end_date - start_date).days + 1
            st.metric("Days Requested", f"{days_requested} days")
        
        reason = st.text_area("Reason for Leave", placeholder="Provide a brief reason for your request")
        
        # Validation
        col1, col2, col3 = st.columns(3)
        with col1:
            if start_date > end_date:
                st.error("End date must be after start date")
            elif days_requested > max_days:
                st.error(f"Requested days ({days_requested}) exceed maximum ({max_days}) for {leave_type}")
            else:
                st.success(f"✓ Valid request ({days_requested} days within limit of {max_days})")
        
        # Get the appropriate balance
        if leave_type == "Annual Leave":
            current_balance = balance['annual']
        elif leave_type == "Sick Leave":
            current_balance = balance['sick']
        else:
            current_balance = balance['personal']
        
        with col2:
            if days_requested > current_balance:
                st.warning(f"⚠️ Insufficient balance (You have {current_balance} days)")
            else:
                st.success(f"✓ Balance available ({current_balance} days)")
        
        submitted = st.form_submit_button("✅ Submit Request", use_container_width=True)
        
        if submitted:
            if not reason.strip():
                st.error("Please provide a reason for your leave")
            elif days_requested > current_balance:
                st.error(f"Insufficient balance. You have {current_balance} days available.")
            elif days_requested > max_days:
                st.error(f"Days requested exceed maximum of {max_days} days for {leave_type}")
            elif start_date > end_date:
                st.error("Invalid date range")
            else:
                # Create new request
                new_request_id = f"LR{str(len(leave_requests_df) + 1).zfill(3)}"
                new_row = pd.DataFrame({
                    'Request_ID': [new_request_id],
                    'Employee_ID': [user_id],
                    'LeaveType_ID': [selected_type['LeaveType_ID']],
                    'Start_Date': [start_date],
                    'End_Date': [end_date],
                    'Reason': [reason],
                    'Status': ['pending'],
                    'Approver_ID': [None],
                    'Days_Requested': [days_requested],
                    'Submission_Date': [datetime.now().date()],
                    'Approval_Date': [None],
                    'Rejection_Reason': [None]
                })
                
                # Update CSV
                leave_requests_df_updated = pd.concat([load_leave_requests(), new_row], ignore_index=True)
                leave_requests_df_updated.to_csv('LeaveRequests.csv', index=False)
                
                st.success(f"✅ Request submitted successfully! (ID: {new_request_id})")
                st.balloons()

# ============================================================================
# MANAGER APPROVAL VIEW
# ============================================================================
def show_manager_approvals():
    st.title("✅ Pending Approvals")
    
    user_id = st.session_state.current_user['id']
    pending = get_pending_requests_for_manager(user_id)
    
    if len(pending) == 0:
        st.info("No pending requests to approve")
        return
    
    st.subheader(f"Pending Requests ({len(pending)})")
    
    for idx, req in pending.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card-container">
            <h4 style="margin-top: 0; color: #1F2937;">{req['Name']} - {req['Name_LeaveType']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**Employee:** {req['Name']}")
                st.write(f"📧 {req['Email']}")
            
            with col2:
                st.write(f"**Duration:** {req['Days_Requested']} days")
                st.write(f"📅 {req['Start_Date']} to {req['End_Date']}")
            
            with col3:
                st.write(f"**Department:** {req['Department']}")
                st.write(f"**Submitted:** {req['Submission_Date']}")
            
            with col4:
                st.write(f"**Reason:**")
                st.write(f"_{req['Reason']}_")
            
            col_a, col_r, col_s = st.columns(3)
            
            with col_a:
                if st.button(f"✅ Approve", key=f"approve_{req['Request_ID']}"):
                    # Update the leave request
                    leave_requests_df_updated = load_leave_requests()
                    mask = leave_requests_df_updated['Request_ID'] == req['Request_ID']
                    leave_requests_df_updated.loc[mask, 'Status'] = 'approved'
                    leave_requests_df_updated.loc[mask, 'Approver_ID'] = user_id
                    leave_requests_df_updated.loc[mask, 'Approval_Date'] = datetime.now().date()
                    leave_requests_df_updated.to_csv('LeaveRequests.csv', index=False)
                    
                    st.success(f"✅ Request {req['Request_ID']} approved!")
                    st.rerun()
            
            with col_r:
                if st.button(f"❌ Reject", key=f"reject_{req['Request_ID']}"):
                    st.session_state[f"show_reject_{req['Request_ID']}"] = True
            
            if st.session_state.get(f"show_reject_{req['Request_ID']}", False):
                rejection_reason = st.text_input(
                    "Reason for rejection",
                    key=f"reason_{req['Request_ID']}"
                )
                if st.button(f"Confirm Rejection", key=f"confirm_reject_{req['Request_ID']}"):
                    leave_requests_df_updated = load_leave_requests()
                    mask = leave_requests_df_updated['Request_ID'] == req['Request_ID']
                    leave_requests_df_updated.loc[mask, 'Status'] = 'rejected'
                    leave_requests_df_updated.loc[mask, 'Approver_ID'] = user_id
                    leave_requests_df_updated.loc[mask, 'Approval_Date'] = datetime.now().date()
                    leave_requests_df_updated.loc[mask, 'Rejection_Reason'] = rejection_reason
                    leave_requests_df_updated.to_csv('LeaveRequests.csv', index=False)
                    
                    st.success(f"❌ Request {req['Request_ID']} rejected")
                    st.rerun()
            
            st.divider()

# ============================================================================
# ADMIN DASHBOARD
# ============================================================================
def show_admin_dashboard():
    st.title("🔧 Admin Dashboard")
    
    # Department Statistics
    st.subheader("Department Overview")
    
    depts = pd.read_csv('DepartmentSummary.csv')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_employees = depts['Total_Employees'].sum()
        st.metric("Total Employees", total_employees, "Across all departments")
    
    with col2:
        total_pending = depts['Pending_Requests'].sum()
        st.metric("Pending Requests", total_pending, "Awaiting approval")
    
    with col3:
        total_approved = depts['Approved_Requests'].sum()
        st.metric("Approved Requests", total_approved, "This period")
    
    with col4:
        total_leave_days = depts['Annual_Leave_Used'].sum()
        st.metric("Leave Days Used", total_leave_days, "Annual leave pool")
    
    st.divider()
    
    # Department Statistics Table
    st.subheader("Department Statistics")
    st.dataframe(depts, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # All Requests
    st.subheader("All Leave Requests")
    all_requests = leave_requests_df.copy()
    all_requests = all_requests.merge(employees_df[['Employee_ID', 'Name']], on='Employee_ID')
    all_requests = all_requests.merge(leave_types_df[['LeaveType_ID', 'Name']], 
                                     on='LeaveType_ID', suffixes=('', '_Type'))
    
    display_admin = all_requests[[
        'Request_ID', 'Name', 'Name_Type', 'Start_Date', 'End_Date', 
        'Days_Requested', 'Status', 'Reason'
    ]].copy()
    display_admin.columns = ['Request ID', 'Employee', 'Leave Type', 'Start', 'End', 
                            'Days', 'Status', 'Reason']
    
    st.dataframe(display_admin, use_container_width=True, hide_index=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
def show_sidebar():
    if st.session_state.is_authenticated:
        user = st.session_state.current_user
        
        st.markdown(f"""
        <div style="padding: 20px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <h3 style="color: white; margin: 0;">👤 {user['name']}</h3>
        <p style="color: #9CA3AF; margin: 5px 0; font-size: 0.9rem;">{user['role'].title()}</p>
        <p style="color: #6B7280; margin: 0; font-size: 0.85rem;">{user['department']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation based on role
        if user['role'] == 'employee':
            page = st.radio(
                "Navigation",
                options=['📊 Dashboard', '📝 New Request'],
                label_visibility="collapsed"
            )
        elif user['role'] == 'manager':
            page = st.radio(
                "Navigation",
                options=['📊 Dashboard', '📝 New Request', '✅ My Approvals'],
                label_visibility="collapsed"
            )
        elif user['role'] == 'admin':
            page = st.radio(
                "Navigation",
                options=['📊 Dashboard', '📝 New Request', '✅ Approvals', '🔧 Admin Panel'],
                label_visibility="collapsed"
            )
        else:
            page = None
        
        st.divider()
        
        if st.button("🔓 Logout", use_container_width=True):
            logout()
            st.rerun()
        
        return page
    
    return None

# ============================================================================
# MAIN APP LOGIC
# ============================================================================
def main():
    if not st.session_state.is_authenticated:
        show_login()
    else:
        page = show_sidebar()
        
        if page == '📊 Dashboard':
            show_employee_dashboard()
        elif page == '📝 New Request':
            show_leave_request_form()
        elif page == '✅ My Approvals':
            show_manager_approvals()
        elif page == '🔧 Admin Panel':
            show_admin_dashboard()

if __name__ == "__main__":
    main()
