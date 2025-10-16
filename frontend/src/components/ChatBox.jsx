import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import Message from "./Message";
import InputBar from "./InputBar";
import ClearButton from "./ClearButton";
import { sendMessage } from "../services/api";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [conversationId] = useState(uuidv4());
  const [isStreaming, setIsStreaming] = useState(false);

  const handleSend = async (userMsg) => {
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsStreaming(true);
    let assistantText = "";

    await sendMessage(
      userMsg,
      conversationId,
      (chunk) => {
        assistantText += chunk;
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "assistant") {
            return [...prev.slice(0, -1), { role: "assistant", content: assistantText }];
          }
          return [...prev, { role: "assistant", content: assistantText }];
        });
      },
      () => setIsStreaming(false),
      (error) => {
        setIsStreaming(false);
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `[Error] ${error}` },
        ]);
      }
    );
  };

  const handleClear = () => setMessages([]);

  return (
    <div className="chat-container">
      <div className="bg-primary text-white text-center py-3 fw-bold fs-5">
        Chatbot PDF Reader
      </div>

      <div className="chat-body">
        {messages.length === 0 ? (
          <p className="text-white text-center mt-5">
            👋 Start by asking something about the document!
          </p>
        ) : (
          messages.map((msg, i) => (
            <Message key={i} role={msg.role} content={msg.content} />
          ))
        )}
      </div>

      <div className="chat-footer">
        <ClearButton onClear={handleClear} />
        <InputBar onSend={handleSend} disabled={isStreaming} />
      </div>
    </div>
  );
}
