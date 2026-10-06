const API_URL = "http://127.0.0.1:8000/api";


// ============================================================
// SEND MESSAGE TO DJANGO
// ============================================================

export async function sendMessage(
  question,
  sessionId
) {
  const response = await fetch(
    `${API_URL}/chat/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question,
        session_id: sessionId,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      data.detail ||
      "AgentForge request failed."
    );
  }

  return data;
}


// ============================================================
// HUMAN REVIEW
// ============================================================

export async function submitHumanReview(
  sessionId,
  action,
  feedback = ""
) {
  const response = await fetch(
    `${API_URL}/human-review/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        session_id: sessionId,
        action,
        feedback,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      data.detail ||
      "Human review request failed."
    );
  }

  return data;
}


// ============================================================
// BACKWARD-COMPATIBILITY WRAPPER
// ============================================================
//
// Your current App.jsx still expects this function.
// We keep it temporarily while moving the frontend
// from simulation → real Django backend.
// ============================================================

export async function continueAfterHumanReview(
  decision,
  feedback,
  updateAgent,
  reviewData
) {
  const sessionId =
    reviewData?.sessionId ||
    reviewData?.session_id;

  if (!sessionId) {
    throw new Error(
      "Session ID is missing for Human Review."
    );
  }

  if (updateAgent) {
    updateAgent(
      "Human Review",
      "running"
    );
  }

  const result =
    await submitHumanReview(
      sessionId,
      decision,
      feedback || ""
    );

  if (updateAgent) {
    updateAgent(
      "Human Review",
      "completed"
    );

    if (
      !result.requires_human_review
    ) {
      updateAgent(
        "Writer",
        "completed"
      );
    }
  }

  return result;
}


// ============================================================
// TEMPORARY COMPATIBILITY FUNCTION
// ============================================================
//
// Your old App.jsx may still import runAgentForge.
// This now calls the REAL Django backend instead of
// the old frontend simulation.
// ============================================================

export async function runAgentForge(
  question,
  updateAgent,
  sessionId
) {
  if (!sessionId) {
    sessionId =
      `agentforge-${Date.now()}`;
  }

  if (updateAgent) {
    updateAgent(
      "Supervisor",
      "running"
    );
  }

  const result =
    await sendMessage(
      question,
      sessionId
    );

  if (updateAgent) {
    updateAgent(
      "Supervisor",
      "completed"
    );

    updateAgent(
      "Planner",
      "completed"
    );

    const route =
      result?.state?.route ||
      result?.review?.route;

    if (route === "research") {
      updateAgent(
        "Research",
        "completed"
      );

      updateAgent(
        "RAG",
        "skipped"
      );

      updateAgent(
        "Coding",
        "skipped"
      );
    }

    else if (route === "rag") {
      updateAgent(
        "Research",
        "skipped"
      );

      updateAgent(
        "RAG",
        "completed"
      );

      updateAgent(
        "Coding",
        "skipped"
      );
    }

    else if (route === "coding") {
      updateAgent(
        "Research",
        "skipped"
      );

      updateAgent(
        "RAG",
        "skipped"
      );

      updateAgent(
        "Coding",
        "completed"
      );
    }

    else if (
      route === "multi_agent"
    ) {
      updateAgent(
        "Research",
        "completed"
      );

      updateAgent(
        "RAG",
        "completed"
      );

      updateAgent(
        "Coding",
        "completed"
      );
    }

    updateAgent(
      "Reviewer",
      result?.review
        ? "completed"
        : "skipped"
    );

    if (
      result.requires_human_review
    ) {
      updateAgent(
        "Human Review",
        "waiting"
      );

      updateAgent(
        "Writer",
        "waiting"
      );
    }
    else {
      updateAgent(
        "Human Review",
        "skipped"
      );

      updateAgent(
        "Writer",
        "completed"
      );
    }
  }

  return {
    ...result,

    // Keep the session available
    // for Human Review.
    session_id:
      result.session_id ||
      sessionId,
  };
}