import { CheckCircle2, Circle, Loader2, AlertCircle, SkipForward, PauseCircle } from "lucide-react";

function AgentStatus({ agents, isRunning }) {
  const getIcon = status => {
    if (status === "running") return <Loader2 size={17} className="spin" />;
    if (status === "completed") return <CheckCircle2 size={17} />;
    if (status === "error") return <AlertCircle size={17} />;
    if (status === "skipped") return <SkipForward size={17} />;
    if (status === "waiting") return <PauseCircle size={17} />;
    return <Circle size={17} />;
  };
  const getText = status => ({ running: "Working...", completed: "Completed", error: "Error", skipped: "Not required", waiting: "Waiting for approval", idle: "Idle" }[status] || "Idle");

  return (
    <div className="agent-status">
      <div className="panel-heading">
        <div><h3>Agent Workflow</h3><p>{isRunning ? "Executing workflow" : "Workflow state"}</p></div>
        <div className={`status-indicator ${isRunning ? "active" : ""}`} />
      </div>
      <div className="agent-list">
        {agents.map((agent, index) => (
          <div key={agent.name} className={`agent-item ${agent.status}`}>
            <div className="agent-icon">{getIcon(agent.status)}</div>
            <div className="agent-info"><span className="agent-name">{agent.name}</span><span className="agent-state">{getText(agent.status)}</span></div>
            {index < agents.length - 1 && <div className="agent-line" />}
          </div>
        ))}
      </div>
      <div className="workflow-info"><span>LangGraph</span><span className="workflow-dot" /><span>AgentForge</span></div>
    </div>
  );
}
export default AgentStatus;
