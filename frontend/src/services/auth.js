import api from './api';

const AUTH_API = '/auth';

export const authService = {
  // Register new user
  register: async (email, username, password, password2) => {
    const response = await api.post(`${AUTH_API}/register/`, {
      email,
      username,
      password,
      password2,
    });
    
    // Tokens are now in httpOnly cookies (set by backend)
    // Only store user data in localStorage
    if (response.data.user) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  // Login user
  login: async (email, password) => {
    await api.post(`${AUTH_API}/login/`, {
      email,
      password,
    });
    
    // Tokens are now in httpOnly cookies (set by backend)
    // Get user profile after login
    const userResponse = await api.get(`${AUTH_API}/user/`);
    localStorage.setItem('user', JSON.stringify(userResponse.data));
    
    return userResponse.data;
  },

  // Logout user
  logout: async () => {
    try {
      // Backend will handle cookie deletion and token blacklisting
      await api.post(`${AUTH_API}/logout/`);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear user data from localStorage
      localStorage.removeItem('user');
      // Cookies are cleared by backend
    }
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get(`${AUTH_API}/user/`);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  // Update user profile
  updateProfile: async (data) => {
    const response = await api.patch(`${AUTH_API}/user/`, data);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  // Get user by ID
  getUserById: async (id) => {
    const response = await api.get(`${AUTH_API}/users/${id}/`);
    return response.data;
  },

  // Get user's threads
  getUserThreads: async (id) => {
    const response = await api.get(`${AUTH_API}/users/${id}/threads/`);
    return response.data;
  },

  // Get user's posts
  getUserPosts: async (id) => {
    const response = await api.get(`${AUTH_API}/users/${id}/posts/`);
    return response.data;
  },

  // Check if user is logged in
  isLoggedIn: () => {
    // Check if user data exists in localStorage
    // Actual authentication is verified by backend via cookies
    return !!localStorage.getItem('user');
  },

  // Get stored user data
  getStoredUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

export default authService;
