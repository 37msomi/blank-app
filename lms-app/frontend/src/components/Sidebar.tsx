import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  FileText,
  CheckSquare,
  BarChart3,
  LogOut,
} from 'lucide-react';

export default function Sidebar() {
  const { user } = useAuth();

  const menuItems = [
    {
      label: 'Dashboard',
      icon: LayoutDashboard,
      href: '/dashboard',
      roles: ['EMPLOYEE', 'MANAGER', 'ADMIN'],
    },
    {
      label: 'Leave Request',
      icon: FileText,
      href: '/leave-request',
      roles: ['EMPLOYEE'],
    },
    {
      label: 'Approvals',
      icon: CheckSquare,
      href: '/approvals',
      roles: ['MANAGER', 'ADMIN'],
    },
    {
      label: 'Analytics',
      icon: BarChart3,
      href: '/analytics',
      roles: ['ADMIN'],
    },
  ];

  const visibleItems = menuItems.filter((item) =>
    item.roles.includes(user?.role || 'EMPLOYEE')
  );

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-8">
        <h1 className="text-2xl font-bold text-primary">LMS</h1>
        <p className="text-sm text-gray-600 mt-1">Leave Management</p>
      </div>

      <nav className="mt-8">
        {visibleItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              to={item.href}
              className="flex items-center px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-primary transition-colors border-l-4 border-transparent hover:border-primary"
            >
              <Icon className="w-5 h-5 mr-3" />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-8 left-0 right-0 px-6">
        <div className="bg-gray-100 rounded-lg p-4 mb-4">
          <p className="text-sm font-semibold text-gray-700">{user?.name}</p>
          <p className="text-xs text-gray-500 mt-1">{user?.role}</p>
        </div>
        <LogoutButton />
      </div>
    </div>
  );
}

function LogoutButton() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <button
      onClick={handleLogout}
      className="w-full flex items-center justify-center px-4 py-2 text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
    >
      <LogOut className="w-4 h-4 mr-2" />
      <span className="font-medium">Logout</span>
    </button>
  );
}
