import { ShieldCheck, Check, RotateCcw } from "lucide-react";

function HumanReview({ review, onDecision }) {
  return (
    <div className="human-review">
      <div className="review-header">
        <div className="review-icon"><ShieldCheck size={21} /></div>
        <div><h3>Human Review Required</h3><p>AgentForge paused the workflow for your approval.</p></div>
      </div>
      <div className="review-meta"><span>Route</span><strong>{review?.route || "coding"}</strong></div>
      <div className="review-label">Generated Result</div>
      <div className="review-code">{review?.code || review?.answer || "Generated result will appear here."}</div>
      <div className="review-actions">
        <button className="approve-button" onClick={() => onDecision("approve")}><Check size={17} />Approve</button>
        <button className="revise-button" onClick={() => onDecision("revise", window.prompt("What should AgentForge revise?", "") || "Please revise the result.")}><RotateCcw size={17} />Request Revision</button>
      </div>
    </div>
  );
}
export default HumanReview;
