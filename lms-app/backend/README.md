# LMS Backend Setup & Installation

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Update DATABASE_URL if needed
```

### 3. Start Database (using Docker)

```bash
docker-compose up -d
```

Or if using local PostgreSQL:
```bash
createdb lms_db
```

### 4. Run Migrations

```bash
npm run migrate
```

### 5. Start Development Server

```bash
npm run dev
```

The API will be available at `http://localhost:5000`

## API Endpoints

All endpoints require authentication via JWT token in the Authorization header.

**Header Format:**
```
Authorization: Bearer <token>
```

### Auth

- `POST /api/auth/login` - Login and get JWT token
  ```json
  { "email": "user@test.com", "password": "password" }
  ```

### Employees

- `GET /api/employees` - List all employees
- `GET /api/employees/:id` - Get employee details

### Leave Types

- `GET /api/leave-types` - List all leave types

### Leave Balances

- `GET /api/leave-balances?employeeId=ID&year=2024` - Get balances for employee

### Leave Requests

- `GET /api/leave-requests` - List all requests
- `GET /api/leave-requests?status=PENDING` - Filter by status
- `GET /api/leave-requests?employeeId=ID` - Get employee's requests
- `POST /api/leave-requests` - Create new request
- `PUT /api/leave-requests/:id/approve` - Approve request
- `PUT /api/leave-requests/:id/reject` - Reject request

## Database Schema

### employees
- id (UUID, PK)
- name (VARCHAR)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- department (VARCHAR)
- position (VARCHAR)
- manager_id (UUID, FK)
- role (VARCHAR: EMPLOYEE, MANAGER, ADMIN)
- created_at, updated_at

### leave_types
- id (UUID, PK)
- name (VARCHAR, UNIQUE)
- max_days (INTEGER)
- requires_approval (BOOLEAN)
- description (TEXT)

### leave_requests
- id (UUID, PK)
- employee_id (UUID, FK)
- leave_type_id (UUID, FK)
- start_date (DATE)
- end_date (DATE)
- reason (TEXT)
- status (VARCHAR: PENDING, APPROVED, REJECTED)
- approver_id (UUID, FK)
- rejection_reason (TEXT)
- created_at, updated_at

### leave_balances
- id (UUID, PK)
- employee_id (UUID, FK)
- leave_type_id (UUID, FK)
- allowed_days (INTEGER)
- used_days (INTEGER)
- year (INTEGER)
- created_at, updated_at

### departments
- id (UUID, PK)
- name (VARCHAR, UNIQUE)

## Sample Data

The following demo users are seeded on startup:

1. **emp@test.com** (EMPLOYEE)
2. **mgr@test.com** (MANAGER)
3. **admin@test.com** (ADMIN)

Default password: `password`

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and DATABASE_URL is correct:
```bash
psql -U user -d lms_db -c "SELECT 1;"
```

### Migrations Failed

Drop the database and restart:
```bash
dropdb lms_db
createdb lms_db
npm run migrate
```

### Port Already in Use

Change PORT in .env:
```
PORT=3001
```
