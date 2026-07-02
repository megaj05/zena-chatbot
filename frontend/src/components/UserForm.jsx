import React, { useState } from "react";

/**
 * UserForm
 * ---------
 * Renders inline inside the chat transcript whenever the backend sets
 * show_form to "lead", "collab", or "session". Field set changes per
 * type, but all three share name/email/phone + a submit handler that
 * posts to POST /api/lead.
 */
export default function UserForm({ formType, formContext, onSubmit, onCancel, submitting }) {
  const [values, setValues] = useState({
    name: "",
    email: "",
    phone: "",
    companyName: "",
    requirement: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!values.name.trim() || !values.email.trim()) {
      setError("Name and email are required.");
      return;
    }
    if (formType === "collab" && !values.companyName.trim()) {
      setError("Company name is required.");
      return;
    }
    setError("");

    const payload = {
      formType,
      name: values.name.trim(),
      email: values.email.trim(),
      phone: values.phone.trim(),
    };

    if (formType === "collab") {
      payload.companyName = values.companyName.trim();
      payload.requirement = values.requirement.trim();
    } else if (formType === "session") {
      payload.purpose = formContext?.purpose || "Mentorship Session";
    } else {
      payload.category = formContext?.category || "General Enquiry";
      payload.requirement = values.requirement.trim();
    }

    onSubmit(payload);
  };

  const titleMap = {
    lead: formContext?.category ? `Tell us about ${formContext.category}` : "Share your details",
    collab: "Business Collaboration",
    session: "Book a Session with Kirthika",
  };

  return (
    <form className="zena-user-form" onSubmit={handleSubmit}>
      <h4 className="zena-form-title">{titleMap[formType] || "Share your details"}</h4>

      <label className="zena-form-label">
        Name
        <input
          className="zena-form-input"
          name="name"
          type="text"
          placeholder="Your full name"
          value={values.name}
          onChange={handleChange}
        />
      </label>

      {formType === "collab" && (
        <label className="zena-form-label">
          Company Name
          <input
            className="zena-form-input"
            name="companyName"
            type="text"
            placeholder="Your company"
            value={values.companyName}
            onChange={handleChange}
          />
        </label>
      )}

      <label className="zena-form-label">
        Email
        <input
          className="zena-form-input"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={values.email}
          onChange={handleChange}
        />
      </label>

      <label className="zena-form-label">
        Phone
        <input
          className="zena-form-input"
          name="phone"
          type="tel"
          placeholder="Your phone number"
          value={values.phone}
          onChange={handleChange}
        />
      </label>

      {formType !== "session" && (
        <label className="zena-form-label">
          {formType === "collab" ? "Collaboration Requirement" : "Requirement"}
          <textarea
            className="zena-form-textarea"
            name="requirement"
            placeholder={
              formType === "collab"
                ? "Tell us about the collaboration you have in mind"
                : "Briefly describe what you need"
            }
            value={values.requirement}
            onChange={handleChange}
            rows={3}
          />
        </label>
      )}

      {error && <p className="zena-form-error">{error}</p>}

      <div className="zena-form-actions">
        <button type="button" className="zena-form-cancel-btn" onClick={onCancel} disabled={submitting}>
          Cancel
        </button>
        <button type="submit" className="zena-form-submit-btn" disabled={submitting}>
          {submitting ? "Sending..." : "Submit"}
        </button>
      </div>
    </form>
  );
}
