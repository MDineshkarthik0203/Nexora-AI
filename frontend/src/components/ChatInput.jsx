import { useRef, useState } from "react";
import { Send, Paperclip } from "lucide-react";

function ChatInput({ onSend, disabled }) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    if (!message.trim() || disabled) return;
    onSend(message);
    setMessage("");
    textareaRef.current?.focus();
  };

  const handleKeyDown = e => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="input-container">
      <div className="chat-input-wrapper">
        <button className="icon-button" title="Attach file" type="button"><Paperclip size={19} /></button>
        <textarea
          ref={textareaRef}
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask AgentForge anything..."
          disabled={disabled}
          rows={1}
        />
        <button className="send-button" onClick={handleSubmit} disabled={disabled || !message.trim()} type="button">
          <Send size={18} />
        </button>
      </div>
      <p className="input-hint">Enter to send · Shift + Enter for new line</p>
    </div>
  );
}
export default ChatInput;