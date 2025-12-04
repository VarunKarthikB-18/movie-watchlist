import axios from 'axios'

// Axios instance with default configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5001',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor: add JWT token to Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor: handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If 401 or 422 (malformed token), clear token and redirect to login
    if (error.response?.status === 401 || error.response?.status === 422) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_id')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export default api
