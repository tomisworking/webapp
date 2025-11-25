import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import forumService from '../services/forum';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';

const Home = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const data = await forumService.getCategories();
      // Handle both array and paginated response
      if (Array.isArray(data)) {
        setCategories(data);
      } else if (data && Array.isArray(data.results)) {
        setCategories(data.results);
      } else if (data && typeof data === 'object') {
        // If it's an object but not paginated, wrap it in an array
        setCategories([data]);
      } else {
        setCategories([]);
      }
    } catch (err) {
      setError('Failed to load categories');
      console.error('Error loading categories:', err);
      setCategories([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Forum Categories</h1>
      </div>

      <ErrorMessage message={error} />

      <div className="categories-grid">
        {categories.map((category) => (
          <Link
            key={category.id}
            to={`/category/${category.slug}`}
            className="category-card"
          >
            <div className="category-icon">{category.icon}</div>
            <div className="category-name">{category.name}</div>
            <div className="category-description">{category.description}</div>
            <div className="category-stats">
              <span>📝 {category.thread_count} threads</span>
              <span>💬 {category.post_count} posts</span>
            </div>
          </Link>
        ))}
      </div>

      {categories.length === 0 && !loading && (
        <div className="card">
          <p style={{ textAlign: 'center', color: '#666' }}>
            No categories available yet.
          </p>
        </div>
      )}
    </div>
  );
};

export default Home;
