import { useAuth } from '../context/AuthContext';
import { Bell, User } from 'lucide-react';

export default function Header() {
  const { user } = useAuth();

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="px-8 py-4 flex justify-between items-center">
        <h2 className="text-gray-800 text-lg font-semibold">Welcome</h2>
        <div className="flex items-center gap-6">
          <button className="relative p-2 text-gray-600 hover:text-gray-900">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <button className="flex items-center gap-2 p-2 text-gray-600 hover:text-gray-900">
            <User className="w-5 h-5" />
            <span className="text-sm font-medium">{user?.email}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
