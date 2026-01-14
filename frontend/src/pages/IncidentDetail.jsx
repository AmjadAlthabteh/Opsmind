import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, AlertTriangle, CheckCircle2, MessageSquare } from 'lucide-react';
import {
  getIncident,
  getIncidentTimeline,
  getIncidentActions,
  getIncidentEvents,
  updateIncidentStatus,
  connectToIncidentRoom,
} from '../services/api';
import { formatDistanceToNow } from 'date-fns';

function IncidentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [incident, setIncident] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [actions, setActions] = useState([]);
  const [events, setEvents] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const wsRef = useRef(null);

  useEffect(() => {
    loadIncidentData();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [id]);

  const loadIncidentData = async () => {
    try {
      const [incidentData, timelineData, actionsData, eventsData] = await Promise.all([
        getIncident(id),
        getIncidentTimeline(id),
        getIncidentActions(id),
        getIncidentEvents(id, 20),
      ]);

      setIncident(incidentData);
      setTimeline(timelineData);
      setActions(actionsData);
      setEvents(eventsData);
    } catch (error) {
      console.error('Failed to load incident:', error);
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    wsRef.current = connectToIncidentRoom(id, (message) => {
      if (message.type === 'user_message') {
        setMessages((prev) => [...prev, message]);
      } else if (message.type === 'connection') {
        console.log(message.message);
      }
    });
  };

  const handleStatusChange = async (newStatus) => {
    try {
      const updated = await updateIncidentStatus(id, newStatus);
      setIncident(updated);
      loadIncidentData(); // Reload to get updated timeline
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading incident...</div>;
  }

  if (!incident) {
    return <div className="empty-state">Incident not found</div>;
  }

  return (
    <div>
      <button
        onClick={() => navigate('/')}
        className="btn"
        style={{ marginBottom: '1.5rem', background: 'var(--bg-secondary)' }}
      >
        <ArrowLeft size={18} />
        Back to Dashboard
      </button>

      <div style={{ display: 'grid', gap: '1.5rem' }}>
        {/* Incident Header */}
        <div className="incidents-list">
          <div style={{ padding: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
              <div>
                <h1 style={{ fontSize: '1.75rem', marginBottom: '0.5rem' }}>{incident.title}</h1>
                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
                  <span className={`badge ${incident.severity}`}>{incident.severity}</span>
                  <span className={`badge ${incident.status}`}>{incident.status}</span>
                </div>
              </div>
            </div>

            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
              {incident.description}
            </p>

            <div style={{ display: 'flex', gap: '1rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                <Clock size={16} />
                Created {formatDistanceToNow(new Date(incident.created_at))} ago
              </div>
              {incident.resolved_at && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <CheckCircle2 size={16} />
                  Resolved in {incident.mttr_minutes?.toFixed(0)}m
                </div>
              )}
            </div>

            {/* Status Actions */}
            {incident.status !== 'resolved' && (
              <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {incident.status === 'open' && (
                  <button
                    onClick={() => handleStatusChange('investigating')}
                    className="btn btn-primary"
                  >
                    Start Investigation
                  </button>
                )}
                {incident.status === 'investigating' && (
                  <>
                    <button
                      onClick={() => handleStatusChange('identified')}
                      className="btn btn-primary"
                    >
                      Mark as Identified
                    </button>
                    <button
                      onClick={() => handleStatusChange('monitoring')}
                      className="btn btn-primary"
                    >
                      Start Monitoring
                    </button>
                  </>
                )}
                {['identified', 'monitoring'].includes(incident.status) && (
                  <button
                    onClick={() => handleStatusChange('resolved')}
                    className="btn btn-primary"
                  >
                    Mark as Resolved
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Two Column Layout */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          {/* Timeline */}
          <div className="incidents-list">
            <div className="section-header">
              <h2 className="section-title">Timeline</h2>
            </div>
            <div style={{ padding: '1rem' }}>
              {timeline.length === 0 ? (
                <div className="empty-state">No timeline entries</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {timeline.map((entry) => (
                    <div key={entry.id} style={{ borderLeft: '2px solid var(--accent-blue)', paddingLeft: '1rem' }}>
                      <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>{entry.title}</div>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>
                        {entry.description}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                        {formatDistanceToNow(new Date(entry.timestamp))} ago • {entry.actor}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="incidents-list">
            <div className="section-header">
              <h2 className="section-title">Suggested Actions</h2>
            </div>
            <div style={{ padding: '1rem' }}>
              {actions.length === 0 ? (
                <div className="empty-state">No actions suggested yet</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {actions.map((action) => (
                    <div
                      key={action.id}
                      style={{
                        padding: '1rem',
                        background: 'var(--bg-tertiary)',
                        borderRadius: '6px',
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <div style={{ fontWeight: 600 }}>{action.title}</div>
                        <span className={`badge ${action.status}`}>{action.status}</span>
                      </div>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        {action.description}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recent Events */}
        <div className="incidents-list">
          <div className="section-header">
            <h2 className="section-title">Recent Events</h2>
          </div>
          <div style={{ padding: '1rem' }}>
            {events.length === 0 ? (
              <div className="empty-state">No events logged</div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {events.map((event) => (
                  <div
                    key={event.id}
                    style={{
                      padding: '0.75rem',
                      background: 'var(--bg-tertiary)',
                      borderRadius: '4px',
                      fontSize: '0.875rem',
                    }}
                  >
                    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.25rem' }}>
                      <span className={`badge ${event.level}`}>{event.level}</span>
                      <span style={{ color: 'var(--text-secondary)' }}>{event.source}</span>
                      <span style={{ color: 'var(--text-secondary)', marginLeft: 'auto' }}>
                        {formatDistanceToNow(new Date(event.timestamp))} ago
                      </span>
                    </div>
                    <div>{event.message}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default IncidentDetail;
