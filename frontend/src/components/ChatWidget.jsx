import React, { useState, useRef, useCallback, useEffect } from "react";
import ChatHeader from "./ChatHeader.jsx";
import ChatMessages from "./ChatMessages.jsx";
import UserForm from "./UserForm.jsx";
import { sendChatMessage, submitLead } from "../services/api.js";

const MAIN_MENU = [
  { id: "explore_services", label: "Explore Services" },
  { id: "training_programs", label: "Training Programs" },
  { id: "business_collaboration", label: "Business Collaboration" },
  { id: "other_enquiries", label: "Other Enquiries" },
];

let idCounter = 0;
const nextId = () => `m${Date.now()}_${idCounter++}`;

function timestamp() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [hasStarted, setHasStarted] = useState(false);
  const [messages, setMessages] = useState([]);
  const [currentNode, setCurrentNode] = useState("start");
  const [isTyping, setIsTyping] = useState(false);
  const [showForm, setShowForm] = useState(null); // null | "lead" | "collab" | "session"
  const [formContext, setFormContext] = useState({});
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [lastQuickReplyId, setLastQuickReplyId] = useState(null);

  const typingTimeout = useRef(null);

  /** Push one or more bot bubbles, attaching quick replies/links only
   * to the final bubble of the batch so they appear under the last line. */
  const pushBotTurn = useCallback((botMessages, quickReplies, links) => {
    const newMsgs = botMessages.map((text, i) => ({
      id: nextId(),
      sender: "bot",
      text,
      timestamp: timestamp(),
      quickReplies: i === botMessages.length - 1 ? quickReplies : undefined,
      links: i === botMessages.length - 1 ? links : undefined,
    }));
    setMessages((prev) => [...prev, ...newMsgs]);
    const last = newMsgs[newMsgs.length - 1];
    setLastQuickReplyId(quickReplies && quickReplies.length > 0 ? last.id : null);
  }, []);

  const pushUserBubble = useCallback((text) => {
    setMessages((prev) => [...prev, { id: nextId(), sender: "user", text, timestamp: timestamp() }]);
  }, []);

  /** Simulate a brief "typing" delay so bot replies don't snap in instantly. */
  const withTypingDelay = useCallback((fn) => {
    setIsTyping(true);
    clearTimeout(typingTimeout.current);
    typingTimeout.current = setTimeout(() => {
      setIsTyping(false);
      fn();
    }, 550 + Math.random() * 400);
  }, []);

  const openChat = () => {
    setIsOpen(true);
    if (!hasStarted) {
      setHasStarted(true);
      withTypingDelay(async () => {
        try {
          const data = await sendChatMessage("start", "menu", "");
          pushBotTurn(data.bot_messages, data.quick_replies, data.links);
          setCurrentNode(data.node);
          setShowForm(data.show_form);
          setFormContext(data.form_context || {});
        } catch (err) {
          pushBotTurn(["Sorry, I couldn't connect to the server. Please make sure the backend is running."]);
        }
      });
    }
  };
  

  const closeChat = () => setIsOpen(false);
  const minimizeChat = () => setIsOpen(false);

  const goToNode = useCallback((node, type, value) => {
    setLastQuickReplyId(null); // lock previous buttons immediately
    withTypingDelay(async () => {
      try {
        const data = await sendChatMessage(node, type, value);
        pushBotTurn(data.bot_messages, data.quick_replies, data.links);
        setCurrentNode(data.node);
        setShowForm(data.show_form);
        setFormContext(data.form_context || {});
      } catch (err) {
        pushBotTurn(["Something went wrong reaching the server. Please try again."]);
      }
    });
  }, [pushBotTurn, withTypingDelay]);

  const handleQuickReply = (id, label) => {
    pushUserBubble(label);
    goToNode(currentNode, "menu", id);
  };

  const handleSendText = () => {
    const text = inputValue.trim();
    if (!text) return;
    pushUserBubble(text);
    setInputValue("");
    goToNode(currentNode, "text", text);
  };

  const handleAttachmentClick = () => {
    setMessages((prev) => [
      ...prev,
      {
        id: nextId(),
        sender: "bot",
        text: "File attachments aren't supported yet — feel free to describe what you need in text instead!",
        timestamp: timestamp(),
      },
    ]);
  };

  const handleFormSubmit = async (payload) => {
    setFormSubmitting(true);
    pushUserBubble(`✅ Submitted: ${payload.name}`);
    try {
      const data = await submitLead(payload);
      setShowForm(null);
      withTypingDelay(() => {
        pushBotTurn(data.bot_messages, data.quick_replies, data.links);
        setCurrentNode(data.node);
      });
    } catch (err) {
      pushBotTurn(["Sorry, I couldn't submit that. Please check your details and try again."]);
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleFormCancel = () => {
    setShowForm(null);
    pushBotTurn(["No worries! What else can I help you with?"], MAIN_MENU);
    setCurrentNode("main_menu");
  };

  return (
    <div className="zena-widget-root">
      {isOpen && (
        <div className="zena-chat-window">
          <ChatHeader onMinimize={minimizeChat} onClose={closeChat} />

          <ChatMessages
            messages={messages}
            isTyping={isTyping}
            onQuickReply={handleQuickReply}
            lastQuickReplyId={lastQuickReplyId}
          />

          {showForm && (
            <div className="zena-form-wrapper">
              <UserForm
                formType={showForm}
                formContext={formContext}
                onSubmit={handleFormSubmit}
                onCancel={handleFormCancel}
                submitting={formSubmitting}
              />
            </div>
          )}

          <div className="zena-input-area">
            <button className="zena-attachment-btn" onClick={handleAttachmentClick} aria-label="Attach file">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <button
  className={`zena-floating-btn ${isOpen ? "zena-floating-btn-hidden" : ""}`}
  onClick={openChat}
  aria-label="Open ZeNA AI Assistant"
>
  <img
    src="/logo.png"
    alt="ZeNA Logo"
    className="zena-logo"
  />
</button>
                <path
                  d="M13.5 7.5l-5 5a2.5 2.5 0 003.54 3.54l5-5a4 4 0 00-5.66-5.66l-5.5 5.5"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
            <input
              type="text"
              className="zena-text-input"
              placeholder="Type your message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendText()}
              disabled={isTyping}
            />
            <button className="zena-send-btn" onClick={handleSendText} aria-label="Send message">
              <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
                <path d="M2 10l16-7-5 16-3-6-8-3z" fill="currentColor" />
              </svg>
            </button>
          </div>
        </div>
      )}

      <button
  className={`zena-floating-btn ${isOpen ? "zena-floating-btn-hidden" : ""}`}
  onClick={openChat}
  aria-label="Open ZeNA AI Assistant"
>
  <img
    src="/logo.png"
    alt="ZeNA Logo"
    className="zena-logo"
  />
</button>
    </div>
  );
}
