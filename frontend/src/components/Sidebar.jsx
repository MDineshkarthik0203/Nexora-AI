import { Plus, MessageSquare, Settings, Github, Sparkles } from "lucide-react";

function Sidebar({ onNewChat }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="brand">
          <div className="brand-icon"><Sparkles size={20} /></div>
          <div><h1>AgentForge</h1><span>AI Engineering Copilot</span></div>
        </div>
        <button className="new-chat-button" onClick={onNewChat}>
          <Plus size={18} /><span>New Chat</span>
        </button>
      </div>
      <div className="sidebar-section">
        <p className="section-title">WORKSPACE</p>
        <button className="sidebar-item active">
          <MessageSquare size={17} /><span>Agent Sessions</span>
        </button>
      </div>
      <div className="sidebar-bottom">
        <button className="sidebar-item"><Github size={17} /><span>GitHub</span></button>
        <button className="sidebar-item"><Settings size={17} /><span>Settings</span></button>
        <div className="version">AgentForge v1.0</div>
      </div>
    </aside>
  );
}
export default Sidebar;