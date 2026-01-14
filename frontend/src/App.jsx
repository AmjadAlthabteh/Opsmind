import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Activity } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import IncidentDetail from './pages/IncidentDetail';
import CreateIncident from './pages/CreateIncident';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="header">
          <div className="header-title">
            <Activity size={32} />
            AI Incident Commander
          </div>
          <nav className="header-nav">
            <NavLink to="/" className="nav-link">Dashboard</NavLink>
            <NavLink to="/create" className="nav-link">Create Incident</NavLink>
          </nav>
        </header>
        <main className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/incident/:id" element={<IncidentDetail />} />
            <Route path="/create" element={<CreateIncident />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
