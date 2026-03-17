# 🚀 LMS Quick Start Guide

## ⚡ 30-Second Setup

### 1. Start Database
```bash
cd lms-app
docker-compose up -d
```

### 2. Start Backend (Terminal 1)
```bash
cd lms-app/backend
npm install
npm run dev
```

### 3. Start Frontend (Terminal 2)
```bash
cd lms-app/frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser! 🎉

---

## 🔓 Login Credentials

Use any of these to test different roles:

```
👤 Employee
   Email: emp@test.com
   Pass:  password

👔 Manager  
   Email: mgr@test.com
   Pass:  password

🔧 Admin
   Email: admin@test.com
   Pass:  password
```

---

## 📍 What Each Role Can Do

### Employee
- View leave balances
- Submit leave requests
- View own request history

### Manager
- View leave balances
- Submit leave requests
- **Approve/Reject pending requests**

### Admin
- Full access to all features
- Future: advanced reporting

---

## 📂 Key Files to Know

| File | Purpose |
|------|---------|
| `/frontend/src/App.tsx` | Main app routing |
| `/frontend/src/pages/*` | All pages (Login, Dashboard, etc.) |
| `/backend/src/server.ts` | API server setup |
| `/backend/src/routes/api.ts` | All API endpoints |

---

## 🔌 API Endpoints

### Login
```bash
POST /api/auth/login
Body: { email, password }
```

### Leave Requests
```bash
GET  /api/leave-requests              # All requests
GET  /api/leave-requests?employeeId=ID
POST /api/leave-requests              # Create
PUT  /api/leave-requests/:id/approve
PUT  /api/leave-requests/:id/reject
```

### Leave Balances
```bash
GET /api/leave-balances?employeeId=ID&year=2024
```

---

## 🎯 Test the System

1. **Login** as Employee: emp@test.com
   - See Dashboard with leave balances
   - Click "Leave Request" → submit a request

2. **Login** as Manager: mgr@test.com
   - Go to "Approvals"
   - See pending requests from employees
   - Click "Review" → approve or reject

3. **Refresh** as Employee
   - See request status changed!

---

## 📁 Project Structure

```
lms-app/
├── frontend/          ← React UI
├── backend/           ← Express API
├── docker-compose.yml ← PostgreSQL
├── GETTING_STARTED.md ← Full setup guide
└── BUILD_SUMMARY.md   ← What was built
```

---

## ❓ Troubleshooting

### "Can't connect to database"
```bash
# Make sure Docker container is running
docker-compose ps

# If not running, start it
docker-compose up -d
```

### "API connection refused"
```bash
# Check backend is running on port 5000
# Verify REACT_APP_API_URL in frontend/.env
```

### "Port 3000 already in use"
```bash
# Use different port
PORT=3001 npm start
```

---

## 🎓 Next Steps

1. **Understand the flow**:
   - Login → Select role
   - View dashboards
   - Submit/approve requests

2. **Explore the code**:
   - Check `/frontend/src/pages/EmployeeDashboard.tsx` - Employee view
   - Check `/backend/src/routes/api.ts` - API endpoints
   - Check `/backend/src/db/migrations.ts` - Database schema

3. **Customize it**:
   - Add more leave types
   - Change colors in `tailwind.config.js`
   - Add new fields to forms
   - Create new pages/components

---

## 📚 Full Documentation

For detailed setup, API docs, and troubleshooting:
- Read `GETTING_STARTED.md` for comprehensive guide
- Read `BUILD_SUMMARY.md` for complete feature list
- Check `frontend/README.md` for frontend specifics
- Check `backend/README.md` for backend specifics

---

## 🎉 You're Ready!

Your Leave Management System is ready to use. Start with the 30-second setup above, then explore the features!

Need help? Check the detailed guides mentioned above.

Happy coding! 🚀
