import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import forumService from '../services/forum';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import { useAuth } from '../context/AuthContext';

const ThreadDetail = () => {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [replyContent, setReplyContent] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [replyError, setReplyError] = useState('');

  useEffect(() => {
    loadThreadWithPosts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const loadThreadWithPosts = async () => {
    try {
      setLoading(true);
      const result = await forumService.getThreadWithPosts(id);
      setData(result);
    } catch (err) {
      setError('Failed to load thread');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReplySubmit = async (e) => {
    e.preventDefault();
    setReplyError('');
    setSubmitting(true);

    try {
      await forumService.createPost({
        thread_id: id,
        content: replyContent,
      });
      setReplyContent('');
      await loadThreadWithPosts();
    } catch (err) {
      setReplyError(
        err.response?.data?.error || 'Failed to post reply. Please try again.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;
  if (!data) return <ErrorMessage message="Thread not found" />;

  const { thread, posts } = data;

  return (
    <div className="container">
      <div style={{ marginTop: '2rem', marginBottom: '1rem' }}>
        <Link to={`/category/${thread.category.slug}`} style={{ color: '#3498db' }}>
          ← Back to {thread.category.name}
        </Link>
      </div>

      {/* Thread */}
      <div className="card">
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '1rem' }}>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 'bold' }}>{thread.title}</h1>
          {thread.is_pinned && <span className="badge badge-pinned">Pinned</span>}
          {thread.is_locked && <span className="badge badge-locked">Locked</span>}
        </div>

        <div className="post-header" style={{ border: 'none', paddingBottom: 0 }}>
          <div className="post-author">
            <span className="post-author-name">{thread.author.username}</span>
          </div>
          <div className="post-date">{formatDate(thread.created_at)}</div>
        </div>

        <div style={{ marginTop: '1rem', lineHeight: '1.6' }}>
          {thread.content}
        </div>

        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #eee', fontSize: '0.875rem', color: '#888' }}>
          <span>👁️ {thread.views_count} views</span>
          <span style={{ margin: '0 1rem' }}>•</span>
          <span>💬 {thread.post_count} replies</span>
        </div>
      </div>

      {/* Posts */}
      <div className="post-list">
        <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          Replies
        </h2>

        {posts.map((post) => (
          <div key={post.id} className="post-item">
            <div className="post-header">
              <div className="post-author">
                <span className="post-author-name">{post.author.username}</span>
              </div>
              <div className="post-date">{formatDate(post.created_at)}</div>
            </div>
            <div className="post-content">{post.content}</div>
            {post.is_edited && (
              <div className="post-edited">Edited {formatDate(post.updated_at)}</div>
            )}
          </div>
        ))}

        {posts.length === 0 && (
          <p style={{ textAlign: 'center', color: '#666', padding: '2rem' }}>
            No replies yet. Be the first to reply!
          </p>
        )}
      </div>

      {/* Reply Form */}
      {isAuthenticated && !thread.is_locked ? (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Post a Reply</h3>
          <ErrorMessage message={replyError} />
          <form onSubmit={handleReplySubmit}>
            <div className="form-group">
              <textarea
                className="form-textarea"
                placeholder="Write your reply..."
                value={replyContent}
                onChange={(e) => setReplyContent(e.target.value)}
                required
                disabled={submitting}
                rows={5}
              />
            </div>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={submitting || !replyContent.trim()}
            >
              {submitting ? 'Posting...' : 'Post Reply'}
            </button>
          </form>
        </div>
      ) : thread.is_locked ? (
        <div className="card" style={{ marginTop: '2rem', textAlign: 'center', color: '#666' }}>
          <p>🔒 This thread is locked and no longer accepts new replies.</p>
        </div>
      ) : (
        <div className="card" style={{ marginTop: '2rem', textAlign: 'center', color: '#666' }}>
          <p>
            <Link to="/login">Login</Link> or <Link to="/register">register</Link> to
            post a reply.
          </p>
        </div>
      )}
    </div>
  );
};

export default ThreadDetail;
