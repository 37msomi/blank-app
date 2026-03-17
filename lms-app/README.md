# LMS - Leave Management System

A modern, full-stack Leave Management System built with React, Node.js/Express, and PostgreSQL.

## Features

- **Employee Dashboard**: View leave balances and submit leave requests
- **Leave Request Form**: Submit new leave requests with dates and reasons
- **Manager Approvals**: Review and approve/reject pending leave requests
- **Admin Dashboard**: Overview of department leave statistics
- **Role-Based Access**: Employee, Manager, and Admin roles
- **Modern UI**: Clean SaaS-style dashboard with Tailwind CSS

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls
- **Lucide React** for icons

### Backend
- **Node.js** with Express
- **TypeScript** for type safety
- **PostgreSQL** for database
- **JWT** for authentication

## Project Structure

```
lms-app/
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── context/      # React context (Auth)
│   │   ├── types/        # TypeScript types
│   │   └── App.tsx       # Main app component
│   ├── package.json
│   └── tailwind.config.js
│
└── backend/           # Express backend
    ├── src/
    │   ├── db/           # Database setup & migrations
    │   ├── routes/       # API routes
    │   ├── controllers/  # Business logic
    │   ├── middleware/   # Auth & other middleware
    │   └── server.ts     # Express app
    └── package.json
```

## Quick Start

### Prerequisites

- Node.js 16+
- PostgreSQL 12+
- npm or yarn

### 1. Setup Database

```bash
# Using Docker (recommended)
docker-compose up -d

# Or install PostgreSQL locally
# Create a database:
# createdb lms_db
```

### 2. Backend Setup

```bash
cd backend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Run database migrations
npm run migrate

# Start the server
npm run dev
```

Server runs on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Start the app
npm start
```

App runs on `http://localhost:3000`

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/lms_db
JWT_SECRET=your-secret-key-change-in-production
PORT=5000
NODE_ENV=development
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:5000
```

## Demo Credentials

- **Employee**: emp@test.com / password
- **Manager**: mgr@test.com / password
- **Admin**: admin@test.com / password

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Employees
- `GET /api/employees` - Get all employees
- `GET /api/employees/:id` - Get employee details

### Leave Types
- `GET /api/leave-types` - Get all leave types

### Leave Balances
- `GET /api/leave-balances?employeeId=:id&year=:year` - Get leave balances

### Leave Requests
- `GET /api/leave-requests` - Get all requests (filtered by status/employee)
- `POST /api/leave-requests` - Create new request
- `PUT /api/leave-requests/:id/approve` - Approve request
- `PUT /api/leave-requests/:id/reject` - Reject request

## Data Model

### Employees
- ID, Name, Email, Department, Position, Manager ID, Role

### Leave Types
- ID, Name, Max Days, Requires Approval, Description

### Leave Requests
- ID, Employee ID, Leave Type ID, Start/End Dates, Status, Approver ID, Reason

### Leave Balances
- ID, Employee ID, Leave Type ID, Allowed Days, Used Days, Year

## Features to Add

- [ ] Email notifications
- [ ] Calendar view for leave requests
- [ ] Advanced analytics & reporting
- [ ] Recurring leave patterns
- [ ] Team view for managers
- [ ] Export to CSV/PDF
- [ ] Mobile app
- [ ] Real-time notifications

## Contributing

1. Create a feature branch
2. Commit your changes
3. Push to the branch
4. Create a Pull Request

## License

MIT
