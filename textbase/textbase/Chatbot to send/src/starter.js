import React from 'react';
import { Link } from 'react-router-dom';
import './starter.css';  // Import styling for starter page

const Starter = () => {
  return (
    <div className="starter">
      <h2>Welcome to your virtual assistant</h2>
      <p>I'm here to assist you.</p>
      <p>Please tell me your symptoms or ask any medical question.</p>
      <Link to="/chat">
        <button className="start-chat-button">Start Chat</button>
      </Link>
    </div>
  );
};

export default Starter;
