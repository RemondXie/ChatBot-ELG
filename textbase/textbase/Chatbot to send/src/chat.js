import React, { useState } from 'react';
import './chat.css';  // Import styling for chat page
import axios from "axios";

const Chat = () => {
  const [messages, setMessages] = useState([
    { text: "Welcome! I'm here to assist you with any medical questions you might have. Please provide your name and age. Say GOODBYE if you want to quit.", sender: "bot" },
  ]);
  const [userInput, setUserInput] = useState("");

function formatOverview(obj) {
  const entries = Object.entries(obj);  // [["Age", 40], ["BMI", 28], ...]
  const formattedPairs = entries.map(([key, val]) => `${key}: ${val}`);
  return formattedPairs.join(", ");
}

const handleSendMessage = async () => {
  if (userInput.trim()) {
    const newMessages = [...messages, { text: userInput, sender: "user" }];
    setMessages(newMessages);
    setUserInput("");

    try {
      const response = await axios.post("http://localhost:4000/chat", { messages: newMessages });
      const botResponse = response.data.botResponse;
      const content = botResponse.content;

      let parsedJson = null;
      try {

        parsedJson = JSON.parse(content);
      } catch (e) {

        console.error("Error parsing GPT JSON:", e);
      }

      if (
        parsedJson &&
        parsedJson.patient_overview !== undefined &&
        parsedJson.diagnosis !== undefined &&
        parsedJson.advice !== undefined
      ) {


        const patientOverviewObj = parsedJson.patient_overview;
        const overviewText = formatOverview(patientOverviewObj);

        const overviewMsg = { text: "Patient Overview: " + overviewText, sender: "bot" };
        const diagnosisMsg = { text: "Diagnosis: " + parsedJson.diagnosis, sender: "bot" };
        const adviceMsg = { text: "Advice: " + parsedJson.advice, sender: "bot" };

        setMessages((prev) => [...prev, overviewMsg, diagnosisMsg, adviceMsg]);
      } else {

        setMessages((prev) => [...prev, { text: content, sender: "bot" }]);
      }

    } catch (error) {
      console.error("Error calling backend API:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Sorry, an error occurred while processing your message.", sender: "bot" },
      ]);
    }
  }
};

  // Handle the Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  // Reset chat
  const handleResetChat = () => {
    setMessages([{ text: "Welcome! I'm here to assist you with any medical questions you might have. Please provide your name and age. Say GOODBYE if you want to quit.", sender: "bot" }]); // Reset to initial state
    setUserInput("");
  };

  return (
    <div className="chat">
      {/* Displaying the welcome message with a larger font */}
      <div className="welcome-message">
        Welcome! I'm here to assist you with any medical questions you might have.
      </div>

      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={message.sender}>
            <strong>{message.sender === "user" ? "Patient:" : "Chatbot:"}</strong>
            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={handleKeyPress}  // Add the key press event listener
          placeholder="Type your message..."
        />
        <button className="send-chat-button" onClick={handleSendMessage}>Send</button>
      </div>

      {/* Reset Button outside the input container */}
      <div className="reset-container">
        <button className="reset-chat-button" onClick={handleResetChat}>Reset Chat</button>
      </div>
    </div>
  );
};

export default Chat;
