import { Bot, User } from "lucide-react";

function ChatMessage({ message }) {
  const isUser = message.role === "user";
  return (
    <div className={`message-row ${isUser ? "user-message" : "assistant-message"}`}>
      <div className="message-avatar">{isUser ? <User size={17} /> : <Bot size={18} />}</div>
      <div className="message-content">
        <div className="message-meta"><strong>{isUser ? "You" : "AgentForge"}</strong><span>{message.timestamp}</span></div>
        <div className="message-text">{message.content}</div>
      </div>
    </div>
  );
}
export default ChatMessage;