import { Circle, Activity } from "lucide-react";

function ChatHeader() {
  return (
    <header className="chat-header">
      <div>
        <h2>Agent Session</h2>
        <div className="connection-status">
          <Circle size={8} fill="currentColor" /><span>Local Agent</span>
        </div>
      </div>
      <div className="system-status"><Activity size={16} /><span>System Ready</span></div>
    </header>
  );
}
export default ChatHeader;