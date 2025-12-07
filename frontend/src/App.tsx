import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GlobalProvider } from './context/GlobalContext';
import Layout from './components/Layout';
import DatePicker from './components/DatePicker';
import Dashboard from './pages/Dashboard';
import ProfitDiagnostic from './pages/ProfitDiagnostic';
import DemandForecast from './pages/DemandForecast';

import OnboardingTour from './components/OnboardingTour';

function App() {
  return (
    <GlobalProvider>
      <Router>
        <OnboardingTour />
        <Layout>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
            <h1>Dashboard Overview</h1>
            <DatePicker />
          </div>

          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profit" element={<ProfitDiagnostic />} />
            <Route path="/demand" element={<DemandForecast />} />
            <Route path="/inventory" element={<div className="card">Inventory Optimizer Coming Soon</div>} />
            <Route path="/supply" element={<div className="card">Supply Chain Coming Soon</div>} />
            <Route path="/alerts" element={<div className="card">Alerts Coming Soon</div>} />
          </Routes>
        </Layout>
      </Router>
    </GlobalProvider>
  );
}

export default App;
