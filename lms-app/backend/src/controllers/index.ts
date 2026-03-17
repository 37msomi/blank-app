import { query } from '../db';
import { generateToken } from '../middleware/auth';
import bcrypt from 'bcrypt';

export const authController = {
  async login(email: string, password: string) {
    try {
      const result = await query(
        'SELECT id, name, email, role, department FROM employees WHERE email = $1',
        [email]
      );

      if (result.rows.length === 0) {
        throw new Error('User not found');
      }

      const user = result.rows[0];
      // In production, verify hashed password
      // For demo, accept any password
      const token = generateToken({
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        departmentId: user.department,
      });

      return {
        token,
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role,
          departmentId: user.department,
        },
      };
    } catch (error) {
      throw error;
    }
  },

  async getCurrentUser(userId: string) {
    try {
      const result = await query(
        'SELECT id, name, email, role, department FROM employees WHERE id = $1',
        [userId]
      );

      if (result.rows.length === 0) {
        throw new Error('User not found');
      }

      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },
};

export const employeeController = {
  async getAll() {
    try {
      const result = await query(
        'SELECT id, name, email, department, position, manager_id FROM employees ORDER BY name'
      );
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  async getById(id: string) {
    try {
      const result = await query(
        'SELECT id, name, email, department, position, manager_id FROM employees WHERE id = $1',
        [id]
      );
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },
};

export const leaveTypeController = {
  async getAll() {
    try {
      const result = await query('SELECT * FROM leave_types ORDER BY name');
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  async getById(id: string) {
    try {
      const result = await query('SELECT * FROM leave_types WHERE id = $1', [id]);
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },
};

export const leaveBalanceController = {
  async getByEmployee(employeeId: string, year?: number) {
    try {
      const currentYear = year || new Date().getFullYear();
      const result = await query(
        `SELECT lb.*, lt.name, lt.max_days FROM leave_balances lb
         JOIN leave_types lt ON lb.leave_type_id = lt.id
         WHERE lb.employee_id = $1 AND lb.year = $2`,
        [employeeId, currentYear]
      );
      return result.rows;
    } catch (error) {
      throw error;
    }
  },
};

export const leaveRequestController = {
  async getAll(status?: string) {
    try {
      let query_str = `
        SELECT lr.*, 
               e.name as employee_name, e.email as employee_email,
               lt.name as leave_type_name,
               a.name as approver_name
        FROM leave_requests lr
        JOIN employees e ON lr.employee_id = e.id
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        LEFT JOIN employees a ON lr.approver_id = a.id
      `;
      const params: any[] = [];

      if (status) {
        query_str += ' WHERE lr.status = $1';
        params.push(status);
      }

      query_str += ' ORDER BY lr.created_at DESC';
      const result = await query(query_str, params);
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  async getByEmployee(employeeId: string) {
    try {
      const result = await query(
        `SELECT lr.*, 
                e.name as employee_name,
                lt.name as leave_type_name,
                a.name as approver_name
         FROM leave_requests lr
         JOIN employees e ON lr.employee_id = e.id
         JOIN leave_types lt ON lr.leave_type_id = lt.id
         LEFT JOIN employees a ON lr.approver_id = a.id
         WHERE lr.employee_id = $1
         ORDER BY lr.created_at DESC`,
        [employeeId]
      );
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  async create(
    employeeId: string,
    leaveTypeId: string,
    startDate: string,
    endDate: string,
    reason: string
  ) {
    try {
      const result = await query(
        `INSERT INTO leave_requests (employee_id, leave_type_id, start_date, end_date, reason, status)
         VALUES ($1, $2, $3, $4, $5, 'PENDING')
         RETURNING *`,
        [employeeId, leaveTypeId, startDate, endDate, reason]
      );
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },

  async approve(requestId: string, approverId: string) {
    try {
      const result = await query(
        `UPDATE leave_requests 
         SET status = 'APPROVED', approver_id = $2, updated_at = CURRENT_TIMESTAMP
         WHERE id = $1
         RETURNING *`,
        [requestId, approverId]
      );
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },

  async reject(requestId: string, rejectionReason: string) {
    try {
      const result = await query(
        `UPDATE leave_requests 
         SET status = 'REJECTED', rejection_reason = $2, updated_at = CURRENT_TIMESTAMP
         WHERE id = $1
         RETURNING *`,
        [requestId, rejectionReason]
      );
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },
};
