import React from 'react';
import { useAuthStore } from '@/store/authStore';
import { Home, Users, Calendar, MessageSquare, Bell, Settings, LogOut } from 'lucide-react';

const DashboardPage: React.FC = () => {
    const { user, logout } = useAuthStore();

    return (
        <div className="min-h-screen bg-dark-950">
            {/* Sidebar */}
            <aside className="fixed left-0 top-0 h-full w-64 bg-dark-900 border-r border-dark-800 p-4">
                <div className="flex items-center space-x-2 mb-8">
                    <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center text-white font-bold">
                        {user?.username.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <div className="font-semibold text-white">{user?.username}</div>
                        <div className="text-xs text-dark-400">{user?.email}</div>
                    </div>
                </div>

                <nav className="space-y-2">
                    <NavItem icon={<Home />} label="Home" active />
                    <NavItem icon={<Users />} label="Communities" />
                    <NavItem icon={<Calendar />} label="Hackathons" />
                    <NavItem icon={<MessageSquare />} label="Messages" />
                    <NavItem icon={<Bell />} label="Notifications" />
                    <NavItem icon={<Settings />} label="Settings" />
                </nav>

                <button
                    onClick={logout}
                    className="absolute bottom-4 left-4 right-4 btn btn-secondary flex items-center justify-center gap-2"
                >
                    <LogOut className="h-4 w-4" />
                    Logout
                </button>
            </aside>

            {/* Main Content */}
            <main className="ml-64 p-8">
                <h1 className="text-3xl font-bold text-white mb-8">
                    Welcome back, {user?.full_name || user?.username}! 👋
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <StatCard title="Communities" value="12" change="+2 this week" />
                    <StatCard title="Hackathons" value="5" change="3 upcoming" />
                    <StatCard title="Reputation" value="1,234" change="+45 this month" />
                </div>

                <div className="card p-6">
                    <h2 className="text-xl font-bold text-white mb-4">Recommended for You</h2>
                    <p className="text-dark-400">
                        Your personalized feed will appear here. Start by joining communities and connecting with other students!
                    </p>
                </div>
            </main>
        </div>
    );
};

const NavItem: React.FC<{ icon: React.ReactNode; label: string; active?: boolean }> = ({
    icon,
    label,
    active,
}) => {
    return (
        <button
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${active
                    ? 'bg-primary-600 text-white'
                    : 'text-dark-400 hover:bg-dark-800 hover:text-white'
                }`}
        >
            <span className="h-5 w-5">{icon}</span>
            <span className="font-medium">{label}</span>
        </button>
    );
};

const StatCard: React.FC<{ title: string; value: string; change: string }> = ({
    title,
    value,
    change,
}) => {
    return (
        <div className="card p-6">
            <div className="text-dark-400 text-sm mb-1">{title}</div>
            <div className="text-3xl font-bold text-white mb-1">{value}</div>
            <div className="text-sm text-green-400">{change}</div>
        </div>
    );
};

export default DashboardPage;
