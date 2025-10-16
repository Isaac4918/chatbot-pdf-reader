const API_URL = import.meta.env.VITE_API_URL;

/**
 * Sends a chat message and streams responses from the backend using EventSource (SSE).
 * @param {string} message - The user's message
 * @param {string} conversationId - Conversation identifier
 * @param {function} onMessage - Callback for streaming content
 * @param {function} onDone - Callback when stream ends
 * @param {function} onError - Callback on error
 */
export const sendMessage = async (message, conversationId, onMessage, onDone, onError) => {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });

    if (!response.ok) {
      const err = await response.json();
      onError(err.error || "Server returned an error.");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      // Process SSE chunks
      chunk.split("\n\n").forEach((line) => {
        if (line.startsWith("data: ")) {
          const json = line.replace("data: ", "").trim();
          if (!json) return;
          const event = JSON.parse(json);

          if (event.type === "content") onMessage(event.content);
          else if (event.type === "done") onDone();
          else if (event.type === "error") onError(event.content);
        }
      });
    }
  } catch (err) {
    console.error("Streaming error:", err);
    onError("Failed to connect to the server.");
  }
};
