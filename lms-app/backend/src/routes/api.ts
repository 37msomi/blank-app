import { Router, Request, Response } from 'express';
import { authMiddleware } from '../middleware/auth';
import {
  authController,
  employeeController,
  leaveTypeController,
  leaveBalanceController,
  leaveRequestController,
} from '../controllers';

const router = Router();

// Auth routes
router.post('/api/auth/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;
    const result = await authController.login(email, password);
    res.json(result);
  } catch (error: any) {
    res.status(401).json({ error: error.message });
  }
});

router.get('/api/auth/me', authMiddleware, async (req: any, res: Response) => {
  try {
    const user = await authController.getCurrentUser(req.user.id);
    res.json(user);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

// Employee routes
router.get('/api/employees', authMiddleware, async (req: Request, res: Response) => {
  try {
    const employees = await employeeController.getAll();
    res.json(employees);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/api/employees/:id', authMiddleware, async (req: Request, res: Response) => {
  try {
    const employee = await employeeController.getById(req.params.id);
    if (!employee) {
      return res.status(404).json({ error: 'Employee not found' });
    }
    res.json(employee);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

// Leave type routes
router.get('/api/leave-types', authMiddleware, async (req: Request, res: Response) => {
  try {
    const types = await leaveTypeController.getAll();
    res.json(types);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/api/leave-types/:id', authMiddleware, async (req: Request, res: Response) => {
  try {
    const type = await leaveTypeController.getById(req.params.id);
    if (!type) {
      return res.status(404).json({ error: 'Leave type not found' });
    }
    res.json(type);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

// Leave balance routes
router.get('/api/leave-balances', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { employeeId, year } = req.query;
    const balances = await leaveBalanceController.getByEmployee(
      employeeId as string,
      year ? parseInt(year as string) : undefined
    );
    res.json(balances);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

// Leave request routes
router.get('/api/leave-requests', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { status, employeeId } = req.query;

    if (employeeId) {
      const requests = await leaveRequestController.getByEmployee(employeeId as string);
      return res.json(requests);
    }

    const requests = await leaveRequestController.getAll(status as string);
    res.json(requests);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/api/leave-requests', authMiddleware, async (req: any, res: Response) => {
  try {
    const { employeeId, leaveTypeId, startDate, endDate, reason } = req.body;
    const request = await leaveRequestController.create(
      employeeId,
      leaveTypeId,
      startDate,
      endDate,
      reason
    );
    res.status(201).json(request);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

router.put('/api/leave-requests/:id/approve', authMiddleware, async (req: any, res: Response) => {
  try {
    const { approverId } = req.body;
    const request = await leaveRequestController.approve(req.params.id, approverId);
    res.json(request);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

router.put('/api/leave-requests/:id/reject', authMiddleware, async (req: any, res: Response) => {
  try {
    const { rejectionReason } = req.body;
    const request = await leaveRequestController.reject(req.params.id, rejectionReason);
    res.json(request);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

export default router;
