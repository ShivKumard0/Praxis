import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  TrendingUp,
  LineChart,
  Package,
  Tags,
  Users,
  Activity,
  AlertTriangle,
  Settings,
  Bell,
  Search,
  Menu,
  X
} from 'lucide-react';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [isSidebarOpen, setIsSidebarOpen] = useState(!isMobile);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (!mobile) setIsSidebarOpen(true);
      else setIsSidebarOpen(false);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: TrendingUp, label: 'Profit Diagnostic', path: '/profit' },
    { icon: LineChart, label: 'Demand Forecast', path: '/forecast' },
    { icon: Package, label: 'Inventory Optimizer', path: '/inventory' },
    { icon: Tags, label: 'Pricing Engine', path: '/pricing' },
    { icon: Users, label: 'CLV & Retention', path: '/clv' },
    { icon: Activity, label: 'Executive Simulator', path: '/simulator' },
    { icon: AlertTriangle, label: 'Alerts & SLA', path: '/alerts' },
  ];

  return (
    <div className="layout">
      {/* Mobile Header */}
      {isMobile && (
        <div className="mobile-header">
          <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="menu-btn">
            {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <div className="logo">Praxis</div>
          <div className="user-avatar">JD</div>
        </div>
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${isSidebarOpen ? 'open' : 'closed'} ${isMobile ? 'mobile' : ''}`}>
        <div className="sidebar-header">
          <div className="logo-icon"></div>
          <span className="logo-text">Praxis</span>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => isMobile && setIsSidebarOpen(false)}
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="nav-item">
            <Settings size={20} />
            <span>Settings</span>
          </div>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isMobile && isSidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setIsSidebarOpen(false)} />
      )}

      {/* Main Content */}
      <main className="main-content">
        {!isMobile && (
          <header className="top-bar">
            <div className="breadcrumbs">
              <span>Platform</span> / <span className="current">{navItems.find(i => i.path === location.pathname)?.label || 'Dashboard'}</span>
            </div>
            <div className="top-actions">
              <div className="search-bar">
                <Search size={18} />
                <input type="text" placeholder="Search metrics, SKUs..." />
              </div>
              <button className="icon-btn"><Bell size={20} /></button>
              <div className="user-profile">
                <div className="user-avatar">JD</div>
                <div className="user-info">
                  <span className="name">John Doe</span>
                  <span className="role">Supply Chain Mgr</span>
                </div>
              </div>
            </div>
          </header>
        )}
        <div className="content-scroll">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
