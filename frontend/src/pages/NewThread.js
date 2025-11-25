import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import forumService from '../services/forum';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';

const NewThread = () => {
  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category_id: '',
  });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await forumService.getCategories();
      // Handle both array and paginated response
      let categoriesArray = [];
      if (Array.isArray(data)) {
        categoriesArray = data;
      } else if (data && Array.isArray(data.results)) {
        categoriesArray = data.results;
      } else if (data && typeof data === 'object') {
        categoriesArray = [data];
      }
      
      setCategories(categoriesArray);
      if (categoriesArray.length > 0) {
        setFormData((prev) => ({ ...prev, category_id: categoriesArray[0].id }));
      }
    } catch (err) {
      setError('Failed to load categories');
      console.error('Error loading categories:', err);
      setCategories([]);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      const thread = await forumService.createThread(formData);
      navigate(`/threads/${thread.id}`);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          err.response?.data?.detail ||
          'Failed to create thread. Please try again.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Create New Thread</h1>
      </div>

      <div className="card">
        <ErrorMessage message={error} />

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="category_id" className="form-label">
              Category *
            </label>
            <select
              id="category_id"
              name="category_id"
              className="form-select"
              value={formData.category_id}
              onChange={handleChange}
              required
              disabled={submitting}
            >
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.icon} {cat.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="title" className="form-label">
              Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              className="form-input"
              placeholder="Enter thread title"
              value={formData.title}
              onChange={handleChange}
              required
              maxLength={200}
              disabled={submitting}
            />
            <small style={{ color: '#888' }}>
              {formData.title.length}/200 characters
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="content" className="form-label">
              Content *
            </label>
            <textarea
              id="content"
              name="content"
              className="form-textarea"
              placeholder="Write your thread content..."
              value={formData.content}
              onChange={handleChange}
              required
              rows={10}
              disabled={submitting}
            />
          </div>

          <div style={{ display: 'flex', gap: '1rem' }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting ? 'Creating...' : 'Create Thread'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate(-1)}
              disabled={submitting}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewThread;
