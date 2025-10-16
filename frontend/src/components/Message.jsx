export default function Message({ role, content }) {
  const isUser = role === "user";
  return (
    <div className={`d-flex ${isUser ? "justify-content-end" : "justify-content-start"} mb-3`}>
      <div
        className={`p-3 rounded-4 shadow-sm ${
          isUser ? "message-user" : "message-assistant"
        }`}
        style={{ maxWidth: "80%", wordWrap: "break-word" }}
      >
        {content}
      </div>
    </div>
  );
}
