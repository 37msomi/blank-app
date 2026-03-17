import { useEffect, useState } from 'react';
import { leaveRequestService } from '../services/api';
import { Button, Card, Badge } from '../components/Shared';
import { useAuth } from '../context/AuthContext';
import type { LeaveRequest } from '../types';

export default function Approvals() {
  const { user } = useAuth();
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [rejectionReason, setRejectionReason] = useState<string>('');
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const res = await leaveRequestService.getPending();
      setRequests(res.data);
    } catch (error) {
      console.error('Failed to fetch pending requests', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: string) => {
    try {
      if (!user) return;
      await leaveRequestService.approve(id, user.id);
      setRequests(requests.filter((r) => r.id !== id));
    } catch (error) {
      console.error('Failed to approve', error);
    }
  };

  const handleReject = async (id: string) => {
    if (!rejectionReason.trim()) return;
    try {
      await leaveRequestService.reject(id, rejectionReason);
      setRequests(requests.filter((r) => r.id !== id));
      setSelectedId(null);
      setRejectionReason('');
    } catch (error) {
      console.error('Failed to reject', error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Pending Approvals</h1>

      {requests.length === 0 ? (
        <Card>
          <p className="text-gray-500 text-center py-8">No pending requests to approve</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {requests.map((request) => (
            <Card key={request.id}>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Employee</p>
                      <p className="font-semibold text-gray-900">{request.employee?.name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Leave Type</p>
                      <p className="font-semibold text-gray-900">{request.leaveType?.name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Duration</p>
                      <p className="font-semibold text-gray-900">
                        {new Date(request.startDate).toLocaleDateString()} -{' '}
                        {new Date(request.endDate).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  {request.reason && (
                    <div className="mt-4 p-3 bg-gray-50 rounded">
                      <p className="text-sm text-gray-600">Reason</p>
                      <p className="text-gray-900">{request.reason}</p>
                    </div>
                  )}
                </div>
              </div>

              {selectedId === request.id ? (
                <div className="mt-4 space-y-4 border-t pt-4">
                  <textarea
                    value={rejectionReason}
                    onChange={(e) => setRejectionReason(e.target.value)}
                    placeholder="Reason for rejection (if rejecting)"
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <div className="flex gap-2">
                    <Button
                      variant="success"
                      onClick={() => handleApprove(request.id)}
                    >
                      Approve
                    </Button>
                    <Button
                      variant="danger"
                      onClick={() => handleReject(request.id)}
                    >
                      Reject
                    </Button>
                    <Button
                      variant="secondary"
                      onClick={() => {
                        setSelectedId(null);
                        setRejectionReason('');
                      }}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="mt-4 flex gap-2">
                  <Button onClick={() => setSelectedId(request.id)}>
                    Review
                  </Button>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
