import React from 'react';
import { Chatbot } from 'react-chatbot-kit';
import 'react-chatbot-kit/build/main.css';
import './Chatbot.css';  // Ensure this file has the correct styling

// Configuration for the chatbot with Light Blue Theme
const config = {
  initialMessages: [
    {
      text: "Welcome to your virtual assistant!",
      sender: "chatbot",
    },
  ],
  customStyles: {
    botMessageBox: {
      backgroundColor: '#A7C7E7',  // Light blue color for bot messages
      color: 'white',
      fontSize: '1.1rem',
      borderRadius: '8px',
      padding: '15px',
      marginBottom: '10px',
      maxWidth: '80%',
    },
    userMessageBox: {
      backgroundColor: '#E1F5FE',  // Lighter blue for user messages
      color: '#333',
      fontSize: '1.1rem',
      borderRadius: '8px',
      padding: '15px',
      marginBottom: '10px',
      maxWidth: '80%',
    },
    chatButton: {
      backgroundColor: '#4FC3F7',  // Light blue button
      color: 'white',
      borderRadius: '5px',
      fontSize: '1rem',
      padding: '10px 20px',
      border: 'none',
      cursor: 'pointer',
      marginTop: '20px',  // Space above the button
      alignSelf: 'center', // Center the button
      transition: 'background-color 0.3s ease', // Smooth transition for color change
    },
  },
};

// ActionProvider: Provides actions based on user input
const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  // Function to handle the Start Chat button click
  const handleStartConversation = () => {
    const message = createChatBotMessage("Please tell me your symptoms or ask any medical question.");
    setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, message], // Add new message
    }));
  };

  return (
    <div className="action-buttons-container">
      {children}
      {/* Initial instructions */}
      <div className="message-container">
        <p>I'm here to assist you.</p>
        <p>Please share your symptoms or ask any medical question.</p>
      </div>
      {/* "Start Chat" button */}
      <button className="chatbot-button" onClick={handleStartConversation}>
        Start Chat
      </button>
    </div>
  );
};

// MessageParser: Parse and respond to messages based on user input
const MessageParser = (message) => {
  if (typeof message === 'string') {
    if (message.toLowerCase().includes("fever") || message.toLowerCase().includes("headache") || message.toLowerCase().includes("fatigue")) {
      return "It seems you might have a common viral infection. It's always best to consult a healthcare professional for a diagnosis.";
    }
  }

  return "I'm here to assist you. Please share your symptoms or medical concerns.";
};

// ChatbotContainer: The main container for the chatbot UI
const ChatbotContainer = () => {
  return (
    <div className="chatbot-container">
      <Chatbot
        config={config}
        actionProvider={ActionProvider}  // Pass ActionProvider to the chatbot
        messageParser={MessageParser}  // Pass MessageParser to handle responses
      />
    </div>
  );
};

export default ChatbotContainer;
