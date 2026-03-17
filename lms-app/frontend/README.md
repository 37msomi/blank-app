# LMS Frontend Setup & Installation

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Update REACT_APP_API_URL if your API is on a different port
```

### 3. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

## Folder Structure

```
src/
├── components/        # Reusable UI components
│   ├── Layout.tsx         # Main layout wrapper
│   ├── Sidebar.tsx        # Navigation sidebar
│   ├── Header.tsx         # Top header
│   ├── Shared.tsx         # Shared UI components (Card, Button, Badge, etc.)
│   └── ProtectedRoute.tsx # Auth guard for routes
├── pages/            # Page components
│   ├── LoginPage.tsx      # Login / authentication
│   ├── EmployeeDashboard.tsx  # Employee dashboard
│   ├── LeaveRequestForm.tsx    # Submit leave request
│   └── Approvals.tsx      # Manager approval view
├── services/         # API services
│   └── api.ts             # Axios instance & API calls
├── context/          # React Context
│   └── AuthContext.tsx    # Authentication context
├── types/            # TypeScript types
│   └── index.ts           # All type definitions
├── App.tsx           # Main app & routing
├── main.jsx          # React entry point
└── index.css         # Global styles & Tailwind imports
```

## Pages

### Login Page
- Email & password authentication
- Shows demo credentials
- Redirects to dashboard on success

### Employee Dashboard
- View leave balances for all leave types
- See personal leave request history with status
- Quick links to submit new request

### Leave Request Form
- Select leave type
- Choose start and end dates
- Add reason for leave
- Submit request

### Manager Approvals
- View all pending leave requests
- See employee name, leave type, duration
- Review reason for leave
- Approve or reject with optional reason

## Components

### Layout
Wraps all authenticated pages with:
- Sidebar navigation (role-based)
- Top header with user info & notifications
- Main content area

### Shared Components
- `Card` - Container component
- `MetricCard` - Dashboard metric display
- `Badge` - Status indicator
- `Button` - Reusable button component

### ProtectedRoute
Guards routes, redirects to login if not authenticated

## Context

### AuthContext
Provides:
- `user` - Current authenticated user
- `token` - JWT token
- `login()` - Login function
- `logout()` - Logout function
- `isAuthenticated` - Boolean flag
- `isLoading` - Loading state

## Services

### API Service (api.ts)
Exports service objects for:
- `authService` - Login, logout, getCurrentUser
- `employeeService` - Get employees
- `leaveTypeService` - Get leave types
- `leaveBalanceService` - Get leave balances
- `leaveRequestService` - Create, approve, reject requests
- `departmentService` - Get department summary

All services:
- Automatically add JWT token to requests
- Use base URL from `REACT_APP_API_URL` env var
- Can be extended with more functions as needed

## Styling

### Tailwind CSS
- Utility-first CSS framework
- Configured in `tailwind.config.js`
- Custom colors in theme

### Global Styles
- `index.css` - Imports Tailwind directives
- Minimal base styling

## Authentication Flow

1. User visits `/login`
2. Enters email & password
3. Clicks login → `authService.login()`
4. Returns JWT token & user data
5. Token stored in localStorage
6. User redirected to `/dashboard`
7. All subsequent requests include token in header
8. ProtectedRoute checks authentication on navigation

## State Management

Currently uses:
- React Context for auth state
- Local component state for forms & UI
- Can be extended with Redux/Zustand if needed

## Build for Production

```bash
npm run build
```

Creates optimized build in `build/` folder for deployment.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `REACT_APP_API_URL` | Backend API base URL |

## Troubleshooting

### API Connection Error
Check `REACT_APP_API_URL` in .env matches backend URL.

### Login Not Working
Ensure backend is running on correct port and `/api/auth/login` endpoint exists.

### Styling Issues
- Rebuild Tailwind: `npm run build`
- Clear browser cache
- Check `tailwind.config.js` for CSS import paths

### CORS Errors
Backend CORS middleware may need adjustment. Check backend `server.ts`.
