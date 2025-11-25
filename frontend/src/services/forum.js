import api from './api';

export const forumService = {
  // Categories
  getCategories: async () => {
    const response = await api.get('/categories/');
    return response.data;
  },

  getCategoryBySlug: async (slug) => {
    const response = await api.get(`/categories/${slug}/`);
    return response.data;
  },

  getCategoryThreads: async (slug) => {
    const response = await api.get(`/categories/${slug}/threads/`);
    return response.data;
  },

  // Threads
  getThreads: async (params = {}) => {
    const response = await api.get('/threads/', { params });
    return response.data;
  },

  getThreadById: async (id) => {
    const response = await api.get(`/threads/${id}/`);
    return response.data;
  },

  getThreadWithPosts: async (id) => {
    const response = await api.get(`/threads/${id}/posts/`);
    return response.data;
  },

  createThread: async (data) => {
    const response = await api.post('/threads/create/', data);
    return response.data;
  },

  updateThread: async (id, data) => {
    const response = await api.patch(`/threads/${id}/`, data);
    return response.data;
  },

  deleteThread: async (id) => {
    const response = await api.delete(`/threads/${id}/`);
    return response.data;
  },

  // Posts
  getPosts: async (params = {}) => {
    const response = await api.get('/posts/', { params });
    return response.data;
  },

  createPost: async (data) => {
    const response = await api.post('/posts/create/', data);
    return response.data;
  },

  updatePost: async (id, data) => {
    const response = await api.patch(`/posts/${id}/`, data);
    return response.data;
  },

  deletePost: async (id) => {
    const response = await api.delete(`/posts/${id}/`);
    return response.data;
  },
};

export default forumService;
