import axios, { AxiosInstance } from 'axios';
import type {
  Employee,
  LeaveType,
  LeaveRequest,
  LeaveBalance,
  DepartmentSummary,
  AuthResponse,
} from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth Service
export const authService = {
  login: (email: string, password: string) =>
    api.post<AuthResponse>('/auth/login', { email, password }),
  logout: () => localStorage.removeItem('token'),
  getCurrentUser: () => api.get('/auth/me'),
};

// Employee Service
export const employeeService = {
  getAll: () => api.get<Employee[]>('/employees'),
  getById: (id: string) => api.get<Employee>(`/employees/${id}`),
  create: (data: Partial<Employee>) => api.post<Employee>('/employees', data),
  update: (id: string, data: Partial<Employee>) =>
    api.put<Employee>(`/employees/${id}`, data),
};

// Leave Type Service
export const leaveTypeService = {
  getAll: () => api.get<LeaveType[]>('/leave-types'),
  getById: (id: string) => api.get<LeaveType>(`/leave-types/${id}`),
};

// Leave Balance Service
export const leaveBalanceService = {
  getById: (employeeId: string) =>
    api.get<LeaveBalance[]>(`/leave-balances?employeeId=${employeeId}`),
  getByYear: (employeeId: string, year: number) =>
    api.get<LeaveBalance[]>(`/leave-balances?employeeId=${employeeId}&year=${year}`),
};

// Leave Request Service
export const leaveRequestService = {
  getAll: () => api.get<LeaveRequest[]>('/leave-requests'),
  getById: (id: string) => api.get<LeaveRequest>(`/leave-requests/${id}`),
  getByEmployee: (employeeId: string) =>
    api.get<LeaveRequest[]>(`/leave-requests?employeeId=${employeeId}`),
  getPending: () => api.get<LeaveRequest[]>('/leave-requests?status=PENDING'),
  create: (data: Partial<LeaveRequest>) =>
    api.post<LeaveRequest>('/leave-requests', data),
  approve: (id: string, approverId: string) =>
    api.put<LeaveRequest>(`/leave-requests/${id}/approve`, { approverId }),
  reject: (id: string, rejectionReason: string) =>
    api.put<LeaveRequest>(`/leave-requests/${id}/reject`, { rejectionReason }),
};

// Department Summary Service
export const departmentService = {
  getSummary: (departmentId: string) =>
    api.get<DepartmentSummary>(`/departments/${departmentId}/summary`),
};

export default api;
