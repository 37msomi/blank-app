import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { leaveBalanceService, leaveRequestService } from '../services/api';
import { MetricCard, Card, Badge } from '../components/Shared';
import { Calendar, AlertCircle } from 'lucide-react';
import type { LeaveBalance, LeaveRequest } from '../types';

export default function EmployeeDashboard() {
  const { user } = useAuth();
  const [balances, setBalances] = useState<LeaveBalance[]>([]);
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (user) {
          const [balancesRes, requestsRes] = await Promise.all([
            leaveBalanceService.getById(user.id),
            leaveRequestService.getByEmployee(user.id),
          ]);
          setBalances(balancesRes.data);
          setRequests(requestsRes.data);
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Leave Balances</h1>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {balances.map((balance) => (
          <MetricCard
            key={balance.id}
            label={`${balance.leaveTypeId} Remaining`}
            value={balance.remainingDays}
            icon={<Calendar className="w-6 h-6" />}
            color="blue"
          />
        ))}
      </div>

      {/* Recent Requests */}
      <Card>
        <h2 className="text-xl font-bold text-gray-900 mb-6">Your Leave Requests</h2>
        {requests.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No leave requests yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                    Start Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                    End Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {requests.map((request) => (
                  <tr key={request.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {request.leaveType?.name || request.leaveTypeId}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {new Date(request.startDate).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {new Date(request.endDate).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <Badge
                        variant={
                          request.status === 'APPROVED'
                            ? 'success'
                            : request.status === 'REJECTED'
                              ? 'danger'
                              : 'warning'
                        }
                      >
                        {request.status}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
