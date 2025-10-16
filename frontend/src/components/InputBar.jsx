import { useState } from "react";

export default function InputBar({ onSend, disabled }) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSend(message);
    setMessage("");
  };

  return (
    <form onSubmit={handleSubmit} className="chat-footer p-3">
      <div className="input-group">
        <input
          type="text"
          className="form-control"
          placeholder="Ask something about the document..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={disabled}
        />
        <button className="btn btn-primary" type="submit" disabled={disabled}>
          Send
        </button>
      </div>
    </form>
  );
}
