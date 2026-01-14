import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { createIncident } from '../services/api';

function CreateIncident() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    severity: 'medium',
    source: 'manual',
    tags: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const tags = formData.tags
        .split(',')
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0);

      const incident = await createIncident({
        ...formData,
        tags,
      });

      navigate(`/incident/${incident.id}`);
    } catch (err) {
      setError('Failed to create incident. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

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

      <div className="incidents-list" style={{ maxWidth: '800px' }}>
        <div className="section-header">
          <h2 className="section-title">Create New Incident</h2>
        </div>

        <form onSubmit={handleSubmit} style={{ padding: '1.5rem' }}>
          {error && (
            <div
              style={{
                padding: '1rem',
                background: 'rgba(239, 68, 68, 0.1)',
                border: '1px solid var(--accent-red)',
                borderRadius: '6px',
                marginBottom: '1rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: 'var(--accent-red)',
              }}
            >
              <AlertCircle size={20} />
              {error}
            </div>
          )}

          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="title"
              style={{
                display: 'block',
                marginBottom: '0.5rem',
                fontWeight: 600,
              }}
            >
              Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              minLength={5}
              maxLength={200}
              placeholder="Brief description of the incident"
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                fontSize: '1rem',
              }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="description"
              style={{
                display: 'block',
                marginBottom: '0.5rem',
                fontWeight: 600,
              }}
            >
              Description *
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              minLength={10}
              rows={5}
              placeholder="Detailed description of the incident, symptoms, and impact"
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                fontSize: '1rem',
                fontFamily: 'inherit',
                resize: 'vertical',
              }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="severity"
              style={{
                display: 'block',
                marginBottom: '0.5rem',
                fontWeight: 600,
              }}
            >
              Severity *
            </label>
            <select
              id="severity"
              name="severity"
              value={formData.severity}
              onChange={handleChange}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                fontSize: '1rem',
              }}
            >
              <option value="critical">Critical - Total system outage</option>
              <option value="high">High - Major feature broken</option>
              <option value="medium">Medium - Minor feature impacted</option>
              <option value="low">Low - Small issue</option>
              <option value="info">Info - Informational</option>
            </select>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="source"
              style={{
                display: 'block',
                marginBottom: '0.5rem',
                fontWeight: 600,
              }}
            >
              Source
            </label>
            <input
              type="text"
              id="source"
              name="source"
              value={formData.source}
              onChange={handleChange}
              placeholder="manual, datadog, pagerduty, etc."
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                fontSize: '1rem',
              }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="tags"
              style={{
                display: 'block',
                marginBottom: '0.5rem',
                fontWeight: 600,
              }}
            >
              Tags
            </label>
            <input
              type="text"
              id="tags"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="database, api, production (comma-separated)"
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                fontSize: '1rem',
              }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%' }}
          >
            {loading ? 'Creating...' : 'Create Incident'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default CreateIncident;
