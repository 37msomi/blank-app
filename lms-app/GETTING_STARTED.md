# Leave Management System - Getting Started Guide

## Overview

This is a complete Leave Management System built with:
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Node.js/Express + PostgreSQL
- **Authentication**: JWT-based

## System Requirements

- Node.js 16 or higher
- PostgreSQL 12 or higher (or Docker)
- npm or yarn
- 2GB free disk space

## Installation Steps

### Option 1: Automated Setup (Recommended)

#### On macOS/Linux:
```bash
cd lms-app
chmod +x setup.sh
./setup.sh
```

#### On Windows:
```cmd
cd lms-app
setup.bat
```

### Option 2: Manual Setup

#### 1. Start PostgreSQL Database

Using Docker (recommended):
```bash
cd lms-app
docker-compose up -d
```

Or using local PostgreSQL:
```bash
createdb lms_db
```

#### 2. Setup Backend

```bash
cd lms-app/backend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Run database migrations
npm run migrate

# Start the server
npm run dev
```

Backend will run on `http://localhost:5000`

#### 3. Setup Frontend

Open a new terminal:

```bash
cd lms-app/frontend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Start the app
npm start
```

Frontend will open at `http://localhost:3000`

## Demo Access

After everything is running, you can login with:

| Role | Email | Password |
|------|-------|----------|
| Employee | emp@test.com | password |
| Manager | mgr@test.com | password |
| Admin | admin@test.com | password |

## Project Structure

```
lms-app/
├── frontend/                 # React frontend app
│   ├── src/
│   │   ├── components/       # UI components (Layout, Sidebar, etc.)
│   │   ├── pages/            # Page components (Dashboard, Forms, etc.)
│   │   ├── services/         # API client services
│   │   ├── context/          # React Context (Authentication)
│   │   ├── types/            # TypeScript type definitions
│   │   └── App.tsx           # Main App component
│   ├── package.json
│   ├── tailwind.config.js
│   └── README.md
│
├── backend/                  # Express API server
│   ├── src/
│   │   ├── db/               # Database connection & migrations
│   │   ├── controllers/      # Business logic handlers
│   │   ├── routes/           # API routes
│   │   ├── middleware/       # Authentication & validation
│   │   └── server.ts         # Express app setup
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── docker-compose.yml        # PostgreSQL Docker container config
├── setup.sh                  # Linux/macOS setup script
├── setup.bat                 # Windows setup script
└── README.md                 # Main documentation
```

## Key Features

### 👤 Employee Dashboard
- View leave balances for all leave types (Annual, Sick, Personal)
- See personal leave request history
- Check request status (Pending, Approved, Rejected)

### 📝 Leave Request Submission
- Submit new leave requests
- Select leave type and dates
- Add reason for the request
- Real-time form validation

### ✅ Manager Approvals
- View all pending leave requests
- See employee details and request reason
- Approve requests
- Reject with optional reason

### 🏢 Admin Features
- View all system data
- Department-level statistics
- Leave type management
- Extensible for advanced reporting

## Functionality

### Authentication
- Email/password login
- JWT-based sessions (24-hour expiry)
- Role-based access control (EMPLOYEE, MANAGER, ADMIN)
- Automatic token refresh via interceptors

### Leave Management
- Track leave balances by type and employee
- Submit leave requests with flexible date range
- Multi-level approval workflow
- Rejection with reason tracking

### Data Model
- Employees (with manager relationships)
- Leave Types (Annual, Sick, Personal, etc.)
- Leave Requests (with full audit trail)
- Leave Balances (per employee per leave type per year)

## API Endpoints

### Authentication
```
POST   /api/auth/login        # Login & get JWT token
GET    /api/auth/me           # Get current user
```

### Employees
```
GET    /api/employees         # List all employees
GET    /api/employees/:id     # Get employee details
```

### Leave Types
```
GET    /api/leave-types       # List all leave types
GET    /api/leave-types/:id   # Get leave type details
```

### Leave Balances
```
GET    /api/leave-balances?employeeId=:id&year=:year
```

### Leave Requests
```
GET    /api/leave-requests                # All requests
GET    /api/leave-requests?status=PENDING # Filter by status
GET    /api/leave-requests?employeeId=:id # Employee requests
POST   /api/leave-requests                # Create request
PUT    /api/leave-requests/:id/approve    # Approve request
PUT    /api/leave-requests/:id/reject     # Reject request
```

## Environment Configuration

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/lms_db
JWT_SECRET=your-secret-key
PORT=5000
NODE_ENV=development
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

## Available Scripts

### Backend
```bash
npm run dev      # Start development server with auto-reload
npm run build    # Compile TypeScript to JavaScript
npm start        # Run compiled JavaScript
npm run migrate  # Run database migrations
```

### Frontend
```bash
npm start        # Start development server
npm run build    # Build for production
npm test         # Run tests
```

## Database Schema

### Employees Table
- id, name, email, password_hash, department, position, manager_id, role, created_at, updated_at

### Leave Types Table
- id, name, max_days, requires_approval, description, created_at

### Leave Requests Table
- id, employee_id, leave_type_id, start_date, end_date, reason, status, approver_id, rejection_reason, created_at, updated_at

### Leave Balances Table
- id, employee_id, leave_type_id, allowed_days, used_days, year, created_at, updated_at

### Departments Table
- id, name, created_at

## Troubleshooting

### Database Connection Error
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```
**Solution**: Ensure PostgreSQL is running or start Docker container:
```bash
docker-compose up -d
```

### Frontend Can't Connect to API
```
Error: Network Error
```
**Solution**: Check `REACT_APP_API_URL` in frontend `.env` matches backend URL:
```
REACT_APP_API_URL=http://localhost:5000
```

### Migrations Failed
**Solution**: Reset database and retry:
```bash
# Stop and remove Docker container
docker-compose down -v

# Start fresh
docker-compose up -d

# Re-run migrations
npm run migrate
```

### Port Already in Use
**Solution**: Change PORT in backend `.env` or kill process on that port

## Development Tips

### VS Code Extensions Recommended
- REST Client - Test API endpoints
- Thunder Client - Alternative API testing
- MySQL/PostgreSQL - Database explorer

### API Testing
```bash
# Test API endpoint directly
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/employees
```

### Database Query
```bash
# Connect to database
psql -U user -d lms_db

# Useful queries
SELECT * FROM employees;
SELECT * FROM leave_requests;
```

## Future Enhancements

- [ ] Email notifications for requests
- [ ] Calendar view for leave visualization
- [ ] Advanced analytics & reporting
- [ ] Team view for managers
- [ ] Export reports (CSV/PDF)
- [ ] Mobile application
- [ ] Real-time notifications
- [ ] Approval workflow customization
- [ ] Leave carryover policy
- [ ] Holiday calendar integration

## Support

For issues or questions, refer to:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## License

MIT License - feel free to use for any purpose
