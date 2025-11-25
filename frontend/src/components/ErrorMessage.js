import React from 'react';

const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <div className="error-message">
      {typeof message === 'string' ? message : 'An error occurred. Please try again.'}
    </div>
  );
};

export default ErrorMessage;
