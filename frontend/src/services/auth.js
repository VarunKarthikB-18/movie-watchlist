import api from './api.js'

/**
 * Auth service: handles user registration, login, logout, and token management
 */

/**
 * Register a new user
 */
export const register = async (email, password) => {
  const response = await api.post('/auth/register', { email, password })
  return response.data
}

/**
 * Login user and store JWT token
 */
export const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password })
  const { access_token, user_id } = response.data
  
  // Store token and user ID in localStorage
  setToken(access_token)
  setUserId(user_id)
  
  return response.data
}

/**
 * Get stored JWT token from localStorage
 */
export const getToken = () => {
  return localStorage.getItem('access_token')
}

/**
 * Set JWT token in localStorage
 */
export const setToken = (token) => {
  localStorage.setItem('access_token', token)
}

/**
 * Get stored user ID from localStorage
 */
export const getUserId = () => {
  return localStorage.getItem('user_id')
}

/**
 * Set user ID in localStorage
 */
export const setUserId = (userId) => {
  localStorage.setItem('user_id', userId)
}

/**
 * Clear authentication data from localStorage
 */
export const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_id')
}

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return !!getToken()
}
