import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, Clock, CheckCircle, TrendingUp } from 'lucide-react';
import { getIncidents } from '../services/api';
import { formatDistanceToNow } from 'date-fns';

function Dashboard() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadIncidents();
    // Refresh every 30 seconds
    const interval = setInterval(loadIncidents, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadIncidents = async () => {
    try {
      const data = await getIncidents();
      setIncidents(data);
    } catch (error) {
      console.error('Failed to load incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    total: incidents.length,
    open: incidents.filter(i => i.status === 'open' || i.status === 'investigating').length,
    resolved: incidents.filter(i => i.status === 'resolved').length,
    avgMttr: incidents
      .filter(i => i.mttr_minutes)
      .reduce((acc, i) => acc + i.mttr_minutes, 0) /
      Math.max(incidents.filter(i => i.mttr_minutes).length, 1),
  };

  if (loading) {
    return <div className="loading">Loading incidents...</div>;
  }

  return (
    <div className="dashboard">
      <h1 style={{ marginBottom: '1.5rem', fontSize: '2rem' }}>Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">
            <AlertCircle size={20} />
            Total Incidents
          </div>
          <div className="stat-value">{stats.total}</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">
            <Clock size={20} />
            Active Incidents
          </div>
          <div className="stat-value" style={{ color: 'var(--accent-orange)' }}>
            {stats.open}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">
            <CheckCircle size={20} />
            Resolved
          </div>
          <div className="stat-value" style={{ color: 'var(--accent-green)' }}>
            {stats.resolved}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">
            <TrendingUp size={20} />
            Avg MTTR
          </div>
          <div className="stat-value">
            {stats.avgMttr.toFixed(0)}m
          </div>
        </div>
      </div>

      <div className="incidents-list" style={{ marginTop: '2rem' }}>
        <div className="section-header">
          <h2 className="section-title">Recent Incidents</h2>
        </div>
        {incidents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📊</div>
            <p>No incidents yet. Create one to get started.</p>
          </div>
        ) : (
          incidents.map((incident) => (
            <div
              key={incident.id}
              className="incident-item"
              onClick={() => navigate(`/incident/${incident.id}`)}
            >
              <div className="incident-info">
                <div className="incident-title">{incident.title}</div>
                <div className="incident-meta">
                  Created {formatDistanceToNow(new Date(incident.created_at))} ago
                  {incident.tags.length > 0 && (
                    <span> • {incident.tags.join(', ')}</span>
                  )}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <span className={`badge ${incident.severity}`}>
                  {incident.severity}
                </span>
                <span className={`badge ${incident.status}`}>
                  {incident.status}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Dashboard;
