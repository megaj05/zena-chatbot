import React from "react";

/**
 * QuickReplies
 * -------------
 * Renders the rounded pill buttons that appear under a bot message
 * (e.g. main menu options, Yes/No, service list). Disabled once the
 * user has already acted on this message, so old buttons don't stay
 * clickable forever as the conversation scrolls on.
 */
export default function QuickReplies({ options, onSelect, disabled }) {
  if (!options || options.length === 0) return null;

  return (
    <div className="zena-quick-replies">
      {options.map((opt) => (
        <button
          key={opt.id}
          className="zena-quick-reply-btn"
          disabled={disabled}
          onClick={() => onSelect(opt.id, opt.label)}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
