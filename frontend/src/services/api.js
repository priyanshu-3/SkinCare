import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Auth APIs
export const login = async (email, password) => {
  const formData = new FormData();
  formData.append('email', email);
  formData.append('password', password);
  
  const response = await axios.post(`${API_BASE_URL}/login`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    withCredentials: true,
  });
  return response.data;
};

export const register = async (name, email, password, role = 'patient') => {
  const formData = new FormData();
  formData.append('name', name);
  formData.append('email', email);
  formData.append('password', password);
  formData.append('role', role);
  
  const response = await axios.post(`${API_BASE_URL}/register`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    withCredentials: true,
  });
  return response.data;
};

export const logout = async () => {
  const response = await axios.get(`${API_BASE_URL}/logout`, {
    withCredentials: true,
  });
  return response.data;
};

// Analysis APIs
export const analyzeImage = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    withCredentials: true,
  });
  return response.data;
};

export const captureImage = async (imageData) => {
  const response = await api.post('/capture', {
    image: imageData,
  });
  return response.data;
};

// Helper function to get full image URL
export const getImageUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http')) return path;
  return `${API_BASE_URL}${path}`;
};

export default api;

