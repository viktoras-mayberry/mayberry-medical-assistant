import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      if (window.location.pathname !== '/login') {
        toast.error('Session expired. Please log in again.');
        window.location.href = '/login';
      }
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.');
    } else if (error.response?.data?.detail) {
      toast.error(error.response.data.detail);
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getProfile: () => api.get('/auth/me'),
};

// Medical API
export const medicalAPI = {
  chat: (message) => api.post('/medical/chat', message),
  analyzeSymptoms: (symptoms) => api.post('/medical/symptom-checker', symptoms),
  requestSecondOpinion: (request) => api.post('/medical/second-opinion', request),
  analyzeLabResults: (upload) => api.post('/medical/lab-analysis', upload),
};

// Health API
export const healthAPI = {
  check: () => api.get('/health'),
  root: () => api.get('/'),
};

export default api;
