import React from "react";
import ChatWidget from "./components/ChatWidget.jsx";
import "./styles/chatbot.css";

export default function App() {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        margin: 0,
        padding: 0,
        overflow: "hidden",
      }}
    >
      <ChatWidget />
    </div>
  );
}