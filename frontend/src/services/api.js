import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout for all requests
});

// Add request interceptor for retry logic
let retryCount = 0;
const MAX_RETRIES = 3;

api.interceptors.request.use(
  (config) => {
    config.metadata = { startTime: Date.now() };
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for better error handling and retry logic
api.interceptors.response.use(
  (response) => {
    retryCount = 0; // Reset on success
    return response;
  },
  async (error) => {
    const { config } = error;

    // Retry logic for network errors and 5xx server errors
    if (
      config &&
      retryCount < MAX_RETRIES &&
      (!error.response || error.response.status >= 500)
    ) {
      retryCount++;
      console.warn(`Retrying request (${retryCount}/${MAX_RETRIES})...`);

      // Exponential backoff: 1s, 2s, 4s
      await new Promise((resolve) => setTimeout(resolve, Math.pow(2, retryCount - 1) * 1000));

      return api(config);
    }

    retryCount = 0;
    const errorMessage = error.response?.data?.detail || error.message || 'An unexpected error occurred';
    console.error('API Error:', errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
);

// Incidents
export const getIncidents = async (status = null) => {
  const params = status ? { status } : {};
  const response = await api.get('/api/incidents/', { params });
  return response.data;
};

export const getIncident = async (incidentId) => {
  const response = await api.get(`/api/incidents/${incidentId}`);
  return response.data;
};

export const createIncident = async (incidentData) => {
  const response = await api.post('/api/incidents/', incidentData);
  return response.data;
};

export const updateIncidentStatus = async (incidentId, status) => {
  const response = await api.patch(`/api/incidents/${incidentId}/status`, null, {
    params: { status },
  });
  return response.data;
};

export const getIncidentTimeline = async (incidentId) => {
  const response = await api.get(`/api/incidents/${incidentId}/timeline`);
  return response.data;
};

export const getIncidentActions = async (incidentId) => {
  const response = await api.get(`/api/incidents/${incidentId}/actions`);
  return response.data;
};

// Events
export const getIncidentEvents = async (incidentId, limit = 100) => {
  const response = await api.get(`/api/ingest/events/${incidentId}`, {
    params: { limit },
  });
  return response.data;
};

export const ingestEvent = async (eventData) => {
  const response = await api.post('/api/ingest/events', eventData);
  return response.data;
};

// WebSocket
export const connectToIncidentRoom = (incidentId, onMessage) => {
  const wsBaseUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');
  const wsUrl = `${wsBaseUrl}/ws/incidents/${incidentId}`;
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log(`Connected to incident room: ${incidentId}`);
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  ws.onclose = () => {
    console.log('WebSocket connection closed');
  };

  return ws;
};

export default api;
