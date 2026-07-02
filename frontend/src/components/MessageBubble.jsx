import React from "react";

/**
 * MessageBubble
 * --------------
 * Renders a single chat bubble. Bot bubbles are white cards with a
 * purple left border; user bubbles are solid purple, right-aligned.
 * Optionally renders "link buttons" (e.g. Instagram / WhatsApp /
 * Hackathon registration) that open in a new tab.
 */
export default function MessageBubble({ sender, text, timestamp, links }) {
  const isBot = sender === "bot";

  return (
    <div className={`zena-msg-row ${isBot ? "zena-msg-row-bot" : "zena-msg-row-user"}`}>
      <div className={`zena-msg-bubble ${isBot ? "zena-msg-bubble-bot" : "zena-msg-bubble-user"}`}>
        <p className="zena-msg-text">{text}</p>

        {links && links.length > 0 && (
          <div className="zena-msg-links">
            {links.map((link) => (
              <a
                key={link.url}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="zena-msg-link-btn"
              >
                {link.label} ↗
              </a>
            ))}
          </div>
        )}

        {timestamp && <span className="zena-msg-time">{timestamp}</span>}
      </div>
    </div>
  );
}
