const API_BASE_URL = "http://localhost:8000";

function formatHistory(messages) {
  return messages.map((message) => ({
    role:
      message.role === "tutor"
        ? "assistant"
        : "user",
    content: message.content,
  }));
}

export async function sendTutorMessage({
  message,
  history,
  sessionId,
  subject,
}) {
  const response = await fetch(
    `${API_BASE_URL}/api/tutor/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message,
        history: formatHistory(history),
        session_id: sessionId,
        subject: subject,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Unable to contact tutor."
    );
  }

  return data;
}