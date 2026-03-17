# 🔗 LMS Data Relationships - Complete Guide

## Overview

The LMS uses **Pandas DataFrame relationships** (similar to SQL JOINs) to connect data across CSV files.

```
┌──────────────┐         ┌─────────────────┐
│  Employees   │◄────────┤ LeaveRequests   │
│              │         │                 │
│ Employee_ID ◄┤╌╌╌╌╌╌╌╌► Employee_ID     │
└──────────────┘         ├─────────────────┤
                         │ LeaveType_ID    │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  LeaveTypes     │
                         │                 │
                         │ LeaveType_ID ◄──┤
                         └─────────────────┘
```

## 1️⃣ Employee → Employee Relationship

### Purpose
Represents **Manager-to-Employee** relationships (org chart).

### Data Structure

**Employees.csv:**
```
Employee_ID  Manager_ID
E001         (NULL)       ← E001 reports to no one (individual contributor)
E002         (NULL)       ← E002 is a manager (no manager above them)
E004         E002         ← E004 reports to E002
E008         E002         ← E008 reports to E002
E006         (NULL)       ← E006 is a manager
E007         E006         ← E007 reports to E006
```

### How It Works

**Python Code:**
```python
# Find who reports to E002 (manager)
managed_employees = employees_df[employees_df['Manager_ID'] == 'E002']
# Result: E004, E008

# Find who E001's manager is
employee = employees_df[employees_df['Employee_ID'] == 'E001']
manager_id = employee['Manager_ID'].values[0]  # None for E001
```

### Real-World Usage

**Scenario:** Manager E002 logs in
1. App finds all employees where `Manager_ID == 'E002'`
2. Gets: E004, E008
3. Filters LeaveRequests for only these employees
4. Shows only E004 & E008's pending requests
5. Prevents E002 from approving requests from other departments! ✅

## 2️⃣ Employee ← LeaveRequests Relationship

### Purpose
Links **Leave Requests** back to **Employees** (who submitted the request).

### Data Structure

**LeaveRequests.csv:**
```
Request_ID  Employee_ID  Status
LR001       E004         approved    ← Request from E004
LR002       E005         pending     ← Request from E005
LR003       E001         approved    ← Request from E001
LR004       E008         pending     ← Request from E008
```

**Employees.csv:**
```
Employee_ID  Name          Email
E001         Alice Johnson alice@...
E004         David Smith   david@...
E005         Emma Davis    emma@...
E008         Henry Brown   henry@...
```

### How It Works

**Python Code (Merge):**
```python
# Merge to get employee NAMES in request list
merged = leave_requests_df.merge(
    employees_df[['Employee_ID', 'Name']],
    left_on='Employee_ID', 
    right_on='Employee_ID'
)

# Result shows LR001 linked to David Smith instead of just E004
Request_ID  Employee_ID  Status      Name
LR001       E004         approved    David Smith
```

### Real-World Usage

**Scenario:** Admin views dashboard
1. App loads LeaveRequests table
2. Merges with Employees to get names
3. Instead of: `LR001 | E004 | approved`
4. Shows: `LR001 | David Smith | approved` 🎯

## 3️⃣ LeaveType ← LeaveRequests Relationship

### Purpose
Adds **Leave Type name** to requests (Annual, Sick, Personal, etc.).

### Data Structure

**LeaveRequests.csv:**
```
Request_ID  LeaveType_ID  Days_Requested
LR001       LT001         5
LR002       LT001         3
LR003       LT002         1
LR004       LT001         10
```

**LeaveTypes.csv:**
```
LeaveType_ID  Name              Max_Days
LT001         Annual Leave      20
LT002         Sick Leave        10
LT003         Personal Leave    5
```

### How It Works

**Python Code (Merge):**
```python
# Merge to get leave TYPE NAMES
merged = leave_requests_df.merge(
    leave_types_df[['LeaveType_ID', 'Name']],
    left_on='LeaveType_ID',
    right_on='LeaveType_ID'
)

# Result: Shows "Annual Leave" instead of "LT001"
Request_ID  LeaveType_ID  Days  Name
LR001       LT001         5     Annual Leave
```

### Real-World Usage

**Scenario:** Employee submits leave request
1. Form shows dropdown of leave types from LeaveTypes.csv
2. Employee selects "Annual Leave" (LT001)
3. Request saved with LeaveType_ID: LT001
4. Dashboard merges to show: "5 days of Annual Leave"
5. Validation checks: `Days (5) ≤ Max_Days (20)` ✅

## 🔄 Complete Multi-Join Example

### Scenario
Admin views all requests with full details.

**Want to show:**
```
Request ID  Employee Name  Department  Leave Type  Dates  Status
LR001       David Smith    Sales       Annual      ...    Approved
LR002       Emma Davis     Sales       Annual      ...    Pending
```

**Python Code:**
```python
# Start with requests
result = leave_requests_df.copy()

# Add employee names & department
result = result.merge(
    employees_df[['Employee_ID', 'Name', 'Department']],
    left_on='Employee_ID',
    right_on='Employee_ID'
)

# Add leave type names
result = result.merge(
    leave_types_df[['LeaveType_ID', 'Name']],
    left_on='LeaveType_ID',
    right_on='LeaveType_ID',
    suffixes=('', '_LeaveType')  # Distinguish between employee name & type name
)

# Now result has ALL info! ✅
```

## 🎯 Validation Through Relationships

### Example: Check if request exceeds balance

**User submits:** 5 days of Annual Leave

**Validation Logic:**
```python
# 1. Get the request's leave type
leave_type_id = user_request['LeaveType_ID']  # LT001

# 2. Look up max days for this type
leave_type = leave_types_df[leave_types_df['LeaveType_ID'] == leave_type_id]
max_days = leave_type['Max_Days'].values[0]  # 20

# 3. Get employee's balance
employee = employees_df[employees_df['Employee_ID'] == employee_id]
balance = employee['Annual_Leave_Balance'].values[0]  # 15

# 4. Validate
if days_requested <= max_days and days_requested <= balance:
    print("✅ Request approved")  # 5 ≤ 20 AND 5 ≤ 15
else:
    print("❌ Request rejected")
```

## 📊 Manager Filter Example

### Scenario
Manager E002 should only see requests from their team (E004, E008).

**Step 1: Find managed employees**
```python
manager_id = 'E002'
managed_employees = employees_df[
    employees_df['Manager_ID'] == manager_id
]['Employee_ID'].values
# Result: ['E004', 'E008']
```

**Step 2: Filter requests by manager's team**
```python
pending_requests = leave_requests_df[
    (leave_requests_df['Employee_ID'].isin(managed_employees)) &
    (leave_requests_df['Status'] == 'pending')
]
# Result: Only LR002 (E005) and LR004 (E008) if they're pending
```

**Step 3: Enrich with names**
```python
pending_requests = pending_requests.merge(
    employees_df[['Employee_ID', 'Name', 'Email']],
    on='Employee_ID'
)
# Manager sees: "Emma Davis - pending Annual Leave"
```

## 📈 Department Summary Relationship

### Purpose
**Aggregated view** of department-wide metrics.

### Data Structure

**DepartmentSummary.csv:**
```
Department        Total_Employees  Pending_Requests  Approved_Requests
Engineering       3                1                 2
Sales             2                1                 1
Finance           2                0                 1
HR                1                0                 0
```

### How It's Built

**Conceptually** (if calculated on the fly):
```python
# Count employees per department
employees_per_dept = employees_df.groupby('Department').size()

# Count pending requests per department
pending_per_dept = (
    leave_requests_df
    .merge(employees_df[['Employee_ID', 'Department']], 
           left_on='Employee_ID', right_on='Employee_ID')
    .groupby('Department')
    .apply(lambda x: (x['Status'] == 'pending').sum())
)

# Combine into summary
summary = pd.DataFrame({
    'Department': departments,
    'Total_Employees': employees_per_dept,
    'Pending_Requests': pending_per_dept,
    # ... more metrics
})
```

## 🔐 Data Integrity Rules

### Foreign Key Constraints

**Employee IDs must exist:**
```python
# When creating a request with Employee_ID: E999
# This will fail if E999 doesn't exist in Employees.csv
```

**Leave Type IDs must exist:**
```python
# When creating a request with LeaveType_ID: LT999
# This will fail if LT999 doesn't exist in LeaveTypes.csv
```

### Cascading Updates

**If an employee is deleted:**
```python
# Their requests should probably be marked as 'cancelled'
# Or archived, not actually deleted
```

## 🛠️ Hands-On Relationship Testing

### Test 1: Find All Requests for an Employee

```python
import pandas as pd

# Load data
leaves = pd.read_csv('LeaveRequests.csv')
employees = pd.read_csv('Employees.csv')

# Get all requests for E001
e001_requests = leaves[leaves['Employee_ID'] == 'E001']
print(e001_requests)
```

### Test 2: Show Request Details with Names

```python
# Merge to add employee name
requests_with_names = leaves.merge(
    employees[['Employee_ID', 'Name', 'Department']],
    on='Employee_ID'
)
print(requests_with_names[['Request_ID', 'Name', 'Department', 'Status']])
```

### Test 3: Find Manager's Team

```python
# Find employees managed by E002
team_e002 = employees[employees['Manager_ID'] == 'E002']['Employee_ID'].tolist()
# Filter requests from this team
team_requests = leaves[leaves['Employee_ID'].isin(team_e002)]
print(team_requests)
```

## 📝 SQL Equivalent

For those familiar with SQL, here are the Pandas operations mapped:

| Operation | SQL | Pandas |
|-----------|-----|--------|
| Join | `SELECT * FROM A JOIN B ON A.id = B.id` | `A.merge(B, on='id')` |
| Filter | `WHERE status = 'pending'` | `df[df['status'] == 'pending']` |
| Group By | `GROUP BY dept` | `df.groupby('dept')` |
| Count | `COUNT(*)` | `len(df)` or `df.groupby().size()` |

## 🎓 Key Concepts

### 1. Foreign Keys
- Connect tables through shared IDs
- Ensure data consistency
- Enable meaningful joins

### 2. Merging
- SQL JOINs = Pandas `.merge()`
- Combines rows where IDs match
- Brings data from both tables together

### 3. Filtering
- `df[condition]` filters rows
- Multiple conditions with `&` (AND) and `|` (OR)
- Returns subset of data

### 4. Validation
- Check relationships before processing
- Verify IDs exist before creating records
- Prevent orphaned data

## Summary

**The LMS uses three main relationships:**

1. **Employee ↔ Employee:** Manager-subordinate chain
2. **LeaveRequests ← Employee:** Who submitted the request
3. **LeaveRequests ← LeaveType:** What type of leave

**These relationships enable:**
- ✅ Role-based data filtering
- ✅ Rich detail display (names instead of IDs)
- ✅ Validation logic
- ✅ Accurate reporting
- ✅ Data integrity

Pandas handles all the relationship logic! 🐼
