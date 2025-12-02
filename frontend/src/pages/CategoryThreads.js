import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import forumService from '../services/forum';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import { useAuth } from '../context/AuthContext';

const CategoryThreads = () => {
  const { slug } = useParams();
  const { isAuthenticated } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCategoryThreads();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  const loadCategoryThreads = async () => {
    try {
      setLoading(true);
      const result = await forumService.getCategoryThreads(slug);
      setData(result);
    } catch (err) {
      setError('Failed to load threads');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;
  if (!data) return <ErrorMessage message="Category not found" />;

  const { category, threads } = data;

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
            {category.icon}
          </div>
          <h1 className="page-title">{category.name}</h1>
          <p style={{ color: '#666', marginTop: '0.5rem' }}>
            {category.description}
          </p>
        </div>
        {isAuthenticated && (
          <Link to="/threads/new" className="btn btn-primary">
            + New Thread
          </Link>
        )}
      </div>

      <div className="thread-list">
        {threads.map((thread) => (
          <Link
            key={thread.id}
            to={`/threads/${thread.id}`}
            className="thread-item"
          >
            <div className="thread-header">
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <h3 className="thread-title">{thread.title}</h3>
                  {thread.is_pinned && (
                    <span className="badge badge-pinned">Pinned</span>
                  )}
                  {thread.is_locked && (
                    <span className="badge badge-locked">Locked</span>
                  )}
                </div>
                <div className="thread-meta">
                  <span>
                    by <span className="thread-author">{thread.author.username}</span>
                  </span>
                  <span>•</span>
                  <span>{formatDate(thread.created_at)}</span>
                </div>
              </div>
              <div className="thread-stats">
                <span>👁️ {thread.views_count}</span>
                <span>💬 {thread.post_count}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {threads.length === 0 && (
        <div className="card">
          <p style={{ textAlign: 'center', color: '#666' }}>
            No threads in this category yet.
            {isAuthenticated && (
              <>
                {' '}
                <Link to="/threads/new">Create the first one!</Link>
              </>
            )}
          </p>
        </div>
      )}
    </div>
  );
};

export default CategoryThreads;
