import React from "react";

export default function ChatHeader({ onMinimize, onClose }) {
  return (
    <div className="zena-header">
      <div className="zena-header-left">
        <div className="zena-header-logo">
  <img
    src="/logo.png"
    alt="ZeNA Logo"
  />
</div>
      
        <div className="zena-header-text">
          <h2 className="zena-header-title">ZeNA AI Assistant</h2>
          <p className="zena-header-subtitle">Your AI-powered assistant for ZeAI Soft</p>
        </div>
      </div>

      <div className="zena-header-actions">
        <button className="zena-icon-btn" onClick={onMinimize} aria-label="Minimize chat">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </button>
        <button className="zena-icon-btn" onClick={onClose} aria-label="Close chat">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 3L13 13M13 3L3 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </button>
      </div>
    </div>
  );
}
