import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import authService from '../services/auth';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';

const Profile = () => {
  const { user } = useAuth();
  const [threads, setThreads] = useState([]);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('threads');

  useEffect(() => {
    if (user) {
      loadUserData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const loadUserData = async () => {
    try {
      setLoading(true);
      const [threadsData, postsData] = await Promise.all([
        authService.getUserThreads(user.id),
        authService.getUserPosts(user.id),
      ]);
      setThreads(threadsData);
      setPosts(postsData);
    } catch (err) {
      setError('Failed to load profile data');
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

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">My Profile</h1>
      </div>

      <ErrorMessage message={error} />

      {/* User Info Card */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div
            style={{
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2rem',
              color: 'white',
              fontWeight: 'bold',
            }}
          >
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div style={{ flex: 1 }}>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
              {user.username}
            </h2>
            <p style={{ color: '#666', marginBottom: '0.5rem' }}>{user.email}</p>
            {user.bio && <p style={{ color: '#888' }}>{user.bio}</p>}
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#3498db' }}>
              {user.thread_count}
            </div>
            <div style={{ fontSize: '0.875rem', color: '#666' }}>Threads</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#27ae60' }}>
              {user.post_count}
            </div>
            <div style={{ fontSize: '0.875rem', color: '#666' }}>Posts</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ marginTop: '2rem', borderBottom: '2px solid #eee' }}>
        <div style={{ display: 'flex', gap: '2rem' }}>
          <button
            onClick={() => setActiveTab('threads')}
            style={{
              padding: '1rem',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'threads' ? '3px solid #3498db' : 'none',
              color: activeTab === 'threads' ? '#3498db' : '#666',
              fontWeight: activeTab === 'threads' ? 'bold' : 'normal',
              cursor: 'pointer',
              fontSize: '1rem',
            }}
          >
            My Threads ({threads.length})
          </button>
          <button
            onClick={() => setActiveTab('posts')}
            style={{
              padding: '1rem',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'posts' ? '3px solid #3498db' : 'none',
              color: activeTab === 'posts' ? '#3498db' : '#666',
              fontWeight: activeTab === 'posts' ? 'bold' : 'normal',
              cursor: 'pointer',
              fontSize: '1rem',
            }}
          >
            My Posts ({posts.length})
          </button>
        </div>
      </div>

      {/* Content */}
      <div style={{ marginTop: '2rem' }}>
        {activeTab === 'threads' && (
          <div>
            {threads.length === 0 ? (
              <div className="card">
                <p style={{ textAlign: 'center', color: '#666' }}>
                  You haven't created any threads yet.{' '}
                  <Link to="/threads/new">Create your first thread!</Link>
                </p>
              </div>
            ) : (
              <div className="thread-list">
                {threads.map((thread) => (
                  <Link
                    key={thread.id}
                    to={`/threads/${thread.id}`}
                    className="thread-item"
                  >
                    <div className="thread-header">
                      <div style={{ flex: 1 }}>
                        <h3 className="thread-title">{thread.title}</h3>
                        <div className="thread-meta">
                          <span>{thread.category_name}</span>
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
            )}
          </div>
        )}

        {activeTab === 'posts' && (
          <div>
            {posts.length === 0 ? (
              <div className="card">
                <p style={{ textAlign: 'center', color: '#666' }}>
                  You haven't posted any replies yet.
                </p>
              </div>
            ) : (
              <div className="post-list">
                {posts.map((post) => (
                  <div key={post.id} className="post-item">
                    <div style={{ marginBottom: '1rem' }}>
                      <Link
                        to={`/threads/${post.thread_id}`}
                        style={{
                          color: '#3498db',
                          textDecoration: 'none',
                          fontWeight: '500',
                        }}
                      >
                        Re: {post.thread_title}
                      </Link>
                    </div>
                    <div className="post-content">{post.content}</div>
                    <div className="post-date" style={{ marginTop: '0.5rem' }}>
                      {formatDate(post.created_at)}
                      {post.is_edited && <span> • Edited</span>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
