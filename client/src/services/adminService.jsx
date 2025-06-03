import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const adminApi = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
  }
});

export const fetchUsers = async (params) => {
  const response = await adminApi.get('/admin/users', { params });
  return response.data;
};

export const approveUser = async (userId) => {
  const response = await adminApi.post(`/admin/users/${userId}/approve`);
  return response.data;
};

export const rejectUser = async (userId) => {
  const response = await adminApi.post(`/admin/users/${userId}/reject`);
  return response.data;
};