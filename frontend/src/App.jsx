import { useMemo, useState } from "react";
import {
  sendMessage,
  submitHumanReview,
} from "./services/agentforge";
import "./App.css";

/* =========================================================
   ICONS
========================================================= */

function Icon({ name, size = 18 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.8",
    strokeLinecap: "round",
    strokeLinejoin: "round",
  };

  const icons = {
    plus: (
      <>
        <line x1="12" y1="5" x2="12" y2="19" />
        <line x1="5" y1="12" x2="19" y2="12" />
      </>
    ),

    message: (
      <>
        <path d="M20 11.5a7.5 7.5 0 0 1-8 7.5 8.8 8.8 0 0 1-4-.9L4 20l1.3-3.5A7.4 7.4 0 0 1 4 11.5 7.5 7.5 0 0 1 12 4a7.5 7.5 0 0 1 8 7.5Z" />
      </>
    ),

    search: (
      <>
        <circle cx="11" cy="11" r="7" />
        <path d="m20 20-4-4" />
      </>
    ),

    settings: (
      <>
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-1.8 1.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V20h-2.5v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1-1.8-1.8.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.5-1H6v-2.5h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1L9 6.7l.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V5h2.5v.6a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1 1.8 1.8-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.1V14h-.1a1.7 1.7 0 0 0-1.5 1Z" />
      </>
    ),

    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" />
        <path d="M14 2v6h6" />
      </>
    ),

    code: (
      <>
        <path d="m8 9-4 3 4 3" />
        <path d="m16 9 4 3-4 3" />
        <path d="m14 5-4 14" />
      </>
    ),

    image: (
      <>
        <rect x="3" y="4" width="18" height="16" rx="2" />
        <circle cx="8.5" cy="9" r="1.5" />
        <path d="m21 15-5-5L5 20" />
      </>
    ),

    send: (
      <>
        <path d="m22 2-7 20-4-9-9-4Z" />
        <path d="M22 2 11 13" />
      </>
    ),

    chevron: (
      <path d="m7 10 5 5 5-5" />
    ),

    toolbox: (
      <>
        <rect x="3" y="7" width="18" height="13" rx="2" />
        <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
        <path d="M3 12h18" />
      </>
    ),

    database: (
      <>
        <ellipse cx="12" cy="5" rx="8" ry="3" />
        <path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5" />
        <path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7" />
      </>
    ),

    globe: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18" />
        <path d="M12 3a14 14 0 0 1 0 18" />
        <path d="M12 3a14 14 0 0 0 0 18" />
      </>
    ),

    paperclip: (
      <path d="m21.4 11.6-8.8 8.8a6 6 0 0 1-8.5-8.5l9-9a4 4 0 0 1 5.7 5.7l-9 9a2 2 0 0 1-2.8-2.8l8.3-8.3" />
    ),

    copy: (
      <>
        <rect x="8" y="8" width="12" height="12" rx="2" />
        <path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" />
      </>
    ),

    thumbsup: (
      <path d="M7 10v10H4a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2h3Zm0 10h10.2a2 2 0 0 0 1.9-1.4l1.8-6A2 2 0 0 0 19 10h-4l.7-4.1A2.5 2.5 0 0 0 13.2 3L7 10v10Z" />
    ),

    thumbsdown: (
      <path d="M7 14V4H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h3Zm0-10h10.2a2 2 0 0 1 1.9 1.4l1.8 6A2 2 0 0 1 19 14h-4l.7 4.1a2.5 2.5 0 0 1-2.5 2.9L7 14V4Z" />
    ),

    more: (
      <>
        <circle cx="5" cy="12" r="1" fill="currentColor" />
        <circle cx="12" cy="12" r="1" fill="currentColor" />
        <circle cx="19" cy="12" r="1" fill="currentColor" />
      </>
    ),
  };

  return <svg {...common}>{icons[name]}</svg>;
}


/* =========================================================
   LOGO
========================================================= */

function AgentForgeLogo() {
  return (
    <div className="logo-mark">
      <span>✦</span>
    </div>
  );
}


/* =========================================================
   SIDEBAR
========================================================= */

function Sidebar({ onNewChat }) {
  const sessions = [
    {
      title: "Build RAG pipeline",
      time: "2 mins ago",
      active: true,
    },
    {
      title: "Travel Agent Design",
      time: "1 hour ago",
    },
    {
      title: "ResearchPilot Agent",
      time: "3 hours ago",
    },
    {
      title: "LangGraph Debugging",
      time: "5 hours ago",
    },
    {
      title: "ML Project Ideas",
      time: "1 day ago",
    },
  ];

  return (
    <aside className="sidebar">

      <div className="brand">
        <AgentForgeLogo />

        <div>
          <div className="brand-title">AgentForge</div>
          <div className="brand-subtitle">
            AI Engineering Copilot
          </div>
        </div>

        <button className="collapse-button">«</button>
      </div>


      <button
        className="new-chat-button"
        onClick={onNewChat}
      >
        <Icon name="plus" size={21} />
        <span>New Chat</span>
      </button>


      <nav className="main-navigation">

        <div className="nav-item active">
          <Icon name="message" />
          <span>Agent Sessions</span>
        </div>

        <div className="nav-item">
          <span className="nav-symbol">◇</span>
          <span>Templates</span>
        </div>

        <div className="nav-item">
          <Icon name="database" />
          <span>Knowledge Base</span>
        </div>

        <div className="nav-item">
          <Icon name="toolbox" />
          <span>Toolbox</span>
        </div>

        <div className="nav-item">
          <Icon name="settings" />
          <span>Settings</span>
        </div>

      </nav>


      <div className="recent-header">
        <span>RECENT SESSIONS</span>
        <button>+</button>
      </div>


      <div className="session-search">
        <Icon name="search" size={16} />
        <input placeholder="Search sessions..." />
      </div>


      <div className="recent-sessions">

        {sessions.map((session, index) => (
          <div
            key={index}
            className={`recent-session ${
              session.active ? "selected" : ""
            }`}
          >
            <div className="session-icon">
              <Icon name="message" size={17} />
            </div>

            <div className="session-details">
              <div className="session-title">
                {session.title}
              </div>

              <div className="session-time">
                {session.time}
              </div>
            </div>
          </div>
        ))}

      </div>


      <div className="sidebar-bottom">

        <div className="external-link">
          <span className="github-symbol">◉</span>
          GitHub
        </div>

        <div className="external-link">
          <span>▤</span>
          Documentation
        </div>

        <div className="version">
          AgentForge v1.0
        </div>

      </div>

    </aside>
  );
}


/* =========================================================
   HEADER
========================================================= */

function Header() {
  return (
    <header className="topbar">

      <div className="session-heading">

        <div className="session-heading-title">
          Agent Session
        </div>

        <div className="local-agent">
          <span className="online-dot"></span>
          Local Agent
        </div>

      </div>


      <div className="header-controls">

        <button className="model-selector">
          <span className="model-icon">M</span>
          <span>GPT-4o</span>
          <Icon name="chevron" size={14} />
        </button>


        <button className="tools-selector">
          <Icon name="toolbox" size={18} />
          <span>Tools</span>
          <Icon name="chevron" size={14} />
        </button>


        <div className="system-ready">
          <span className="pulse-dot"></span>
          System Ready
        </div>

      </div>

    </header>
  );
}


/* =========================================================
   CHAT MESSAGE
========================================================= */

function AgentMessage({ children }) {
  return (
    <div className="message-row agent-row">

      <div className="agent-avatar">
        ✦
      </div>

      <div className="message-content">

        <div className="message-meta">
          <strong>AgentForge</strong>
          <span>
            {new Date().toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>

        <div className="agent-message">
          {children}
        </div>

      </div>

    </div>
  );
}


function UserMessage({ children }) {
  return (
    <div className="message-row user-row">

      <div className="user-message">
        {children}
      </div>

      <div className="user-avatar">
        M
      </div>

    </div>
  );
}


/* =========================================================
   WELCOME MESSAGE
========================================================= */

function WelcomeMessage() {
  return (
    <AgentMessage>

      <div className="welcome-text">
        New AgentForge session started! 🚀
      </div>

      <div className="welcome-subtitle">
        I can help you with:
      </div>

      <div className="capabilities">

        <div>
          <span>☑</span>
          Building AI agents (LangGraph, LangChain, CrewAI)
        </div>

        <div>
          <span>☑</span>
          RAG systems and LLM applications
        </div>

        <div>
          <span>☑</span>
          Code implementation and debugging
        </div>

        <div>
          <span>☑</span>
          Project architecture and design
        </div>

        <div>
          <span>☑</span>
          Research, planning, and documentation
        </div>

      </div>

      <div className="welcome-question">
        What would you like me to build or research today?
      </div>

    </AgentMessage>
  );
}


/* =========================================================
   PLAN MESSAGE
========================================================= */

function PlanMessage({ result }) {

  const plan =
    result?.state?.plan?.length
      ? result.state.plan
      : [
          "Define architecture and components",
          "Design LangGraph workflow",
          "Implement search and document tools",
          "Generate structured report",
          "Provide complete code and explanation",
        ];

  return (
    <AgentMessage>

      <div className="response-heading">
        Great! I'll help you design a Research Agent using LangGraph.
      </div>

      <div className="plan-heading">
        Here's the plan:
      </div>

      <div className="plan-list">

        {plan.map((item, index) => (
          <div className="plan-item" key={index}>

            <span className="plan-number">
              {index + 1}
            </span>

            <span>
              {item}
            </span>

          </div>
        ))}

      </div>

      <div className="response-ending">
        Let's start with the system architecture.
      </div>

    </AgentMessage>
  );
}


/* =========================================================
   WORKFLOW
========================================================= */

const workflowNodes = [
  {
    key: "supervisor",
    label: "Supervisor",
    description: "Route and analyze query",
  },
  {
    key: "planner",
    label: "Planner",
    description: "Create execution plan",
  },
  {
    key: "research",
    label: "Research",
    description: "Gather information",
  },
  {
    key: "rag",
    label: "RAG",
    description: "Retrieve relevant context",
  },
  {
    key: "coding",
    label: "Coding",
    description: "Generate or analyze code",
  },
  {
    key: "reviewer",
    label: "Reviewer",
    description: "Verify results",
  },
  {
    key: "human",
    label: "Human Review",
    description: "Optional approval",
  },
  {
    key: "writer",
    label: "Writer",
    description: "Generate final output",
  },
];


function WorkflowProgress({ workflow }) {

  const completed = workflow.filter(
    (node) => node.status === "completed"
  ).length;

  const running = workflow.filter(
    (node) => node.status === "running"
  ).length;

  const waiting = workflow.filter(
    (node) => node.status === "waiting"
  ).length;

  const progress = Math.round(
    (completed / workflow.length) * 100
  );

  return (
    <div className="workflow-card">

      <div className="workflow-header">
        <h3>Workflow Progress</h3>
        <span>{progress}%</span>
      </div>

      <div className="progress-bar">
        <div
          className="progress-value"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>


      <div className="workflow-list">

        {workflow.map((node, index) => {

          const isLast =
            index === workflow.length - 1;

          return (
            <div
              className="workflow-item"
              key={node.key}
            >

              <div className="workflow-marker-column">

                <div
                  className={`workflow-marker ${node.status}`}
                >
                  {node.status === "completed" && "✓"}
                  {node.status === "running" && ""}
                  {node.status === "waiting" && ""}
                </div>

                {!isLast && (
                  <div
                    className={`workflow-line ${
                      node.status === "completed"
                        ? "completed"
                        : ""
                    }`}
                  />
                )}

              </div>


              <div className="workflow-text">

                <div className="workflow-label">
                  {node.label}
                </div>

                <div className="workflow-description">
                  {node.description}
                </div>

                {node.status === "running" && (
                  <div className="running-label">
                    Running...
                  </div>
                )}

                {node.status === "waiting" && (
                  <div className="waiting-label">
                    Waiting for approval
                  </div>
                )}

              </div>

            </div>
          );
        })}

      </div>

    </div>
  );
}


/* =========================================================
   TOOLS PANEL
========================================================= */

function ToolsPanel() {

  const tools = [
    {
      icon: "globe",
      name: "Web Search",
    },
    {
      icon: "file",
      name: "Document Reader",
    },
    {
      icon: "code",
      name: "Code Executor",
    },
    {
      icon: "database",
      name: "Vector DB",
    },
    {
      icon: "toolbox",
      name: "Custom Tools",
    },
  ];

  return (
    <div className="tools-card">

      <div className="tools-card-header">
        <h3>Tools</h3>
        <button>Manage</button>
      </div>

      <div className="tools-list">

        {tools.map((tool) => (
          <div className="tool-row" key={tool.name}>

            <div className="tool-name">

              <span className="tool-icon">
                <Icon name={tool.icon} size={16} />
              </span>

              {tool.name}

            </div>

            <span className="tool-status"></span>

          </div>
        ))}

      </div>

    </div>
  );
}


/* =========================================================
   SESSION INFO
========================================================= */

function SessionInfo({ sessionId }) {
  return (
    <div className="session-info-card">

      <h3>Session Info</h3>

      <div className="info-row">
        <span>Session ID</span>
        <strong>{sessionId.slice(0, 18)}</strong>
      </div>

      <div className="info-row">
        <span>Started</span>
        <strong>
          {new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </strong>
      </div>

      <div className="info-row">
        <span>Model</span>
        <strong>GPT-4o</strong>
      </div>

      <div className="info-row">
        <span>Status</span>
        <strong className="status-running">
          <span></span>
          Running
        </strong>
      </div>

    </div>
  );
}


/* =========================================================
   COMPOSER
========================================================= */

function Composer({
  message,
  setMessage,
  onSend,
  loading,
}) {

  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      if (message.trim() && !loading) {
        onSend();
      }
    }
  };


  return (
    <div className="composer-wrapper">

      <div className="composer">

        <button className="attachment-button">
          <Icon name="paperclip" size={19} />
        </button>


        <textarea
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Type your message here..."
          rows={1}
        />


        <div className="composer-toolbar">

          <button className="round-plus">
            <Icon name="plus" size={18} />
          </button>


          <button className="composer-tool active">
            <Icon name="globe" size={15} />
            Web Search
          </button>


          <button className="composer-tool">
            <Icon name="code" size={15} />
            Code
          </button>


          <button className="composer-tool">
            <Icon name="file" size={15} />
            File
          </button>


          <button className="composer-tool">
            <Icon name="image" size={15} />
            Image
          </button>


          <div className="composer-spacer"></div>


          <button className="auto-agent">
            <span>✦</span>
            Auto Agent
            <Icon name="chevron" size={13} />
          </button>


          <button
            className="send-button"
            onClick={onSend}
            disabled={
              loading || !message.trim()
            }
          >
            <Icon name="send" size={19} />
          </button>

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   HUMAN REVIEW
========================================================= */

function HumanReviewPanel({
  review,
  onDecision,
}) {

  const [feedback, setFeedback] =
    useState("");


  if (!review) {
    return null;
  }


  return (
    <div className="review-overlay">

      <div className="review-modal">

        <div className="review-modal-header">

          <div>
            <h2>Human Review Required</h2>
            <p>
              AgentForge is waiting for your approval.
            </p>
          </div>

          <div className="review-status-dot"></div>

        </div>


        <div className="review-content">

          {review.review && (
            <div className="review-section">
              <h4>Reviewer Result</h4>

              <pre>
                {review.review}
              </pre>
            </div>
          )}


          {review.code && (
            <div className="review-section">
              <h4>Generated Code</h4>

              <pre>
                {review.code}
              </pre>
            </div>
          )}


          {review.execution_output && (
            <div className="review-section">
              <h4>Execution Output</h4>

              <pre>
                {review.execution_output}
              </pre>
            </div>
          )}


          <textarea
            className="review-feedback"
            placeholder="Optional revision feedback..."
            value={feedback}
            onChange={(event) =>
              setFeedback(event.target.value)
            }
          />

        </div>


        <div className="review-actions">

          <button
            className="revise-button"
            onClick={() =>
              onDecision("revise", feedback)
            }
          >
            Request Revision
          </button>

          <button
            className="approve-button"
            onClick={() =>
              onDecision("approve", "")
            }
          >
            ✓ Approve
          </button>

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   MAIN APP
========================================================= */

function App() {

  const [sessionId, setSessionId] =
    useState(
      () => `agentforge-${Date.now()}`
    );

  const [message, setMessage] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [review, setReview] =
    useState(null);

  const [error, setError] =
    useState("");


  const [workflow, setWorkflow] =
    useState(
      workflowNodes.map((node) => ({
        ...node,
        status: "pending",
      }))
    );


  const resetWorkflow = () => {

    setWorkflow(
      workflowNodes.map((node) => ({
        ...node,
        status: "pending",
      }))
    );

  };


  const updateWorkflow = (result) => {

    const route =
      result?.state?.route || "";

    const agentPlan =
      result?.state?.agent_plan || [];


    setWorkflow(
      workflowNodes.map((node) => {

        if (node.key === "supervisor") {
          return {
            ...node,
            status: "completed",
          };
        }

        if (node.key === "planner") {

          return {
            ...node,
            status:
              route === "chat"
                ? "completed"
                : "completed",
          };

        }


        if (node.key === "research") {

          return {
            ...node,
            status:
              agentPlan.includes("research") ||
              route === "research"
                ? "completed"
                : "pending",
          };

        }


        if (node.key === "rag") {

          return {
            ...node,
            status:
              agentPlan.includes("rag") ||
              route === "rag"
                ? "completed"
                : "pending",
          };

        }


        if (node.key === "coding") {

          return {
            ...node,
            status:
              agentPlan.includes("coding") ||
              route === "coding"
                ? "completed"
                : "pending",
          };

        }


        if (node.key === "reviewer") {

          return {
            ...node,
            status:
              result?.state?.review
                ? "completed"
                : "pending",
          };

        }


        if (node.key === "human") {

          return {
            ...node,
            status:
              result?.requires_human_review
                ? "waiting"
                : result?.final_answer
                ? "completed"
                : "pending",
          };

        }


        if (node.key === "writer") {

          return {
            ...node,
            status:
              result?.final_answer
                ? "completed"
                : "pending",
          };

        }


        return node;
      })
    );

  };


  const handleSend = async () => {

    if (!message.trim() || loading) {
      return;
    }


    const userMessage = message.trim();

    setMessage("");
    setError("");
    setLoading(true);

    resetWorkflow();


    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        content: userMessage,
      },
    ]);


    try {

      const result =
        await sendMessage(
          userMessage,
          sessionId
        );


      updateWorkflow(result);


      if (
        result.requires_human_review
      ) {

        setReview(
          result.review
        );

        setMessages((previous) => [
          ...previous,
          {
            type: "agent",
            content:
              "I generated a result and it is ready for human review.",
          },
        ]);

      } else {

        setMessages((previous) => [
          ...previous,
          {
            type: "agent",
            content:
              result.final_answer ||
              "AgentForge completed the request.",
            result,
          },
        ]);

      }

    } catch (err) {

      setError(
        err.message ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);

    }

  };


  const handleHumanDecision =
    async (action, feedback) => {

      if (!review) {
        return;
      }


      setLoading(true);
      setError("");


      try {

        const result =
          await submitHumanReview(
            sessionId,
            action,
            feedback
          );


        setReview(null);

        updateWorkflow(result);


        setMessages((previous) => [
          ...previous,
          {
            type: "agent",
            content:
              result.final_answer ||
              "AgentForge completed the revision.",
            result,
          },
        ]);

      } catch (err) {

        setError(
          err.message ||
          "Human review failed."
        );

      } finally {

        setLoading(false);

      }

    };


  const handleNewChat = () => {

    setSessionId(
      `agentforge-${Date.now()}`
    );

    setMessages([]);

    setReview(null);

    setError("");

    resetWorkflow();

  };


  const showWelcome =
    messages.length === 0;


  return (
    <div className="app-shell">

      <Sidebar
        onNewChat={handleNewChat}
      />


      <main className="main-area">

        <Header />


        <div className="workspace">

          <section className="chat-area">

            <div className="chat-scroll">

              {showWelcome && (
                <WelcomeMessage />
              )}


              {messages.map(
                (item, index) => {

                  if (
                    item.type === "user"
                  ) {
                    return (
                      <UserMessage
                        key={index}
                      >
                        {item.content}
                      </UserMessage>
                    );
                  }


                  return (
                    <div
                      key={index}
                      className="agent-response-wrapper"
                    >

                      <AgentMessage>
                        {item.result?.state
                          ?.plan?.length ? (
                          <PlanMessage
                            result={item.result}
                          />
                        ) : (
                          <div className="final-response">
                            {item.content}
                          </div>
                        )}
                      </AgentMessage>


                      <div className="message-actions">

                        <button>
                          <Icon
                            name="copy"
                            size={15}
                          />
                        </button>

                        <button>
                          <Icon
                            name="thumbsup"
                            size={15}
                          />
                        </button>

                        <button>
                          <Icon
                            name="thumbsdown"
                            size={15}
                          />
                        </button>

                        <button>
                          <Icon
                            name="more"
                            size={15}
                          />
                        </button>

                      </div>

                    </div>
                  );
                }
              )}


              {loading && (
                <div className="typing-indicator">

                  <div className="agent-avatar">
                    ✦
                  </div>

                  <div className="typing-bubble">
                    <span></span>
                    <span></span>
                    <span></span>
                    <label>
                      AgentForge is working...
                    </label>
                  </div>

                </div>
              )}


              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}

            </div>


            <Composer
              message={message}
              setMessage={setMessage}
              onSend={handleSend}
              loading={loading}
            />

          </section>


          <aside className="right-panel">

            <WorkflowProgress
              workflow={workflow}
            />

            <ToolsPanel />

            <SessionInfo
              sessionId={sessionId}
            />

          </aside>

        </div>

      </main>


      {review && (
        <HumanReviewPanel
          review={review}
          onDecision={
            handleHumanDecision
          }
        />
      )}

    </div>
  );
}


export default App;