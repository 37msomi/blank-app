// Employee Types
export interface Employee {
  id: string;
  name: string;
  email: string;
  department: string;
  position: string;
  managerId: string | null;
  createdAt: string;
}

export interface LeaveBalance {
  id: string;
  employeeId: string;
  leaveTypeId: string;
  allowedDays: number;
  usedDays: number;
  remainingDays: number;
  year: number;
}

// Leave Type
export interface LeaveType {
  id: string;
  name: string;
  maxDays: number;
  requiresApproval: boolean;
  description: string;
}

// Leave Request
export interface LeaveRequest {
  id: string;
  employeeId: string;
  employee?: Employee;
  leaveTypeId: string;
  leaveType?: LeaveType;
  startDate: string;
  endDate: string;
  reason: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  approverId: string | null;
  approver?: Employee;
  rejectionReason?: string;
  createdAt: string;
  updatedAt: string;
}

// Department Summary
export interface DepartmentSummary {
  id: string;
  name: string;
  totalEmployees: number;
  pendingRequests: number;
  approvedRequests: number;
  leaveBalance: {
    leaveType: string;
    totalAllowed: number;
    totalUsed: number;
  }[];
}

// Auth Types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'EMPLOYEE' | 'MANAGER' | 'ADMIN';
  departmentId: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}
