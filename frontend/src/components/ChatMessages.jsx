import React, { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble.jsx";
import QuickReplies from "./QuickReplies.jsx";

/**
 * ChatMessages
 * -------------
 * Scrollable transcript. Auto-scrolls to the latest message whenever
 * the list grows or the typing indicator toggles. Quick-reply buttons
 * render directly under the bot message that offered them; only the
 * most recent set stays clickable so old menus don't linger active.
 */
export default function ChatMessages({ messages, isTyping, onQuickReply, lastQuickReplyId }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, isTyping]);

  return (
    <div className="zena-messages">
      {messages.map((msg) => (
        <div key={msg.id}>
          <MessageBubble
            sender={msg.sender}
            text={msg.text}
            timestamp={msg.timestamp}
            links={msg.links}
          />
          {msg.quickReplies && msg.quickReplies.length > 0 && (
            <QuickReplies
              options={msg.quickReplies}
              onSelect={onQuickReply}
              disabled={msg.id !== lastQuickReplyId}
            />
          )}
        </div>
      ))}

      {isTyping && (
        <div className="zena-msg-row zena-msg-row-bot">
          <div className="zena-typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
