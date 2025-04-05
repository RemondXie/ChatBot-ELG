import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Starter from './starter';  // Import Starter page from src
import Chat from './chat';        // Import Chat page from src

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Starter />} />  {/* Main page with "Start Chat" */}
        <Route path="/chat" element={<Chat />} />  {/* Chat page where users can chat */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
