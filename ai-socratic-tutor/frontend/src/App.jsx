import { useState } from "react";
import {
  Brain,
  Plus,
  MessageSquare,
  BookOpen,
  BarChart3,
  Settings,
  Send,
  Lightbulb,
  ChevronDown,
  Menu,
  X,
} from "lucide-react";

import { sendTutorMessage } from "./api/tutorApi";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedSubject, setSelectedSubject] =
    useState("Mathematics");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  // Session ID
  const [sessionId] = useState(() =>
    crypto.randomUUID()
  );

  // Loading state
  const [loading, setLoading] = useState(false);

  // Adaptive tutor state
  const [tutorState, setTutorState] = useState({
    action: "guide",
    hint_level: 0,
    attempts: 0,
    solved: false,
    provider: null,
    fallback_used: false,
    latency_ms: null,
  });

  const subjects = [
    "Mathematics",
    "Python",
    "Computer Science",
    "Physics",
  ];

  // --------------------------------------------------
  // Update tutor state
  // --------------------------------------------------

  const updateTutorState = (data) => {
    setTutorState({
      action: data.action ?? "guide",
      hint_level: data.hint_level ?? 0,
      attempts: data.attempts ?? 0,
      solved: data.solved ?? false,
      provider: data.provider ?? null,
      fallback_used: data.fallback_used ?? false,
      latency_ms: data.latency_ms ?? null,
    });
  };

  // --------------------------------------------------
  // Send student message
  // --------------------------------------------------

  const handleSend = async () => {
    if (!input.trim()) return;
    if (loading) return;
    if (tutorState.solved) return;

    const userMessage = input.trim();

    const updatedMessages = [
      ...messages,
      {
        role: "user",
        content: userMessage,
      },
    ];

    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const data = await sendTutorMessage({
        message: userMessage,
        history: messages,
        sessionId,
        subject: selectedSubject,
      });

      setMessages([
        ...updatedMessages,
        {
          role: "tutor",
          content: data.message,
          stage: data.stage,
          action: data.action,
          hint_level: data.hint_level,
          student_understanding:
            data.student_understanding,
          answer_evaluation:
            data.answer_evaluation,
          provider: data.provider,
          fallback_used: data.fallback_used,
          latency_ms: data.latency_ms,
        },
      ]);

      updateTutorState(data);
    } catch (error) {
      console.error("Tutor error:", error);

      setMessages([
        ...updatedMessages,
        {
          role: "tutor",
          content:
            "I'm having trouble connecting right now. Please make sure the tutor backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Request hint
  // --------------------------------------------------

  const handleHint = async () => {
    if (messages.length === 0) return;
    if (loading) return;
    if (tutorState.solved) return;
    if (tutorState.hint_level >= 3) return;

    const hintRequest =
      "I need a hint. Please guide me toward the answer without revealing the complete answer.";

    const updatedMessages = [
      ...messages,
      {
        role: "user",
        content: "I need a hint.",
      },
    ];

    setMessages(updatedMessages);
    setLoading(true);

    try {
      const data = await sendTutorMessage({
        message: hintRequest,
        history: messages,
        sessionId,
        subject: selectedSubject,
      });

      setMessages([
        ...updatedMessages,
        {
          role: "tutor",
          content: data.message,
          stage: data.stage,
          action: data.action,
          hint_level: data.hint_level,
          student_understanding:
            data.student_understanding,
          answer_evaluation:
            data.answer_evaluation,
          provider: data.provider,
          fallback_used: data.fallback_used,
          latency_ms: data.latency_ms,
        },
      ]);

      updateTutorState(data);
    } catch (error) {
      console.error("Hint error:", error);

      setMessages([
        ...messages,
        {
          role: "user",
          content: "I need a hint.",
        },
        {
          role: "tutor",
          content:
            "I couldn't generate a hint right now. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // New session
  // --------------------------------------------------

  const startNewSession = () => {
    if (loading) return;

    setMessages([]);
    setInput("");

    setTutorState({
      action: "guide",
      hint_level: 0,
      attempts: 0,
      solved: false,
      provider: null,
      fallback_used: false,
      latency_ms: null,
    });
  };

  return (
    <div className="app">

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`sidebar ${
          sidebarOpen ? "sidebar-open" : ""
        }`}
      >
        <div className="sidebar-header">
          <div className="brand">
            <div className="brand-icon">
              <Brain size={22} />
            </div>

            <div>
              <h2>Socratic</h2>
              <span>AI Tutor</span>
            </div>
          </div>

          <button
            className="mobile-close"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <button
          className="new-session-btn"
          onClick={startNewSession}
          disabled={loading}
        >
          <Plus size={19} />
          New Session
        </button>

        <nav className="sidebar-nav">

          <div className="nav-section-title">
            WORKSPACE
          </div>

          <button className="nav-item active">
            <MessageSquare size={18} />
            Tutor
          </button>

          <button className="nav-item">
            <BookOpen size={18} />
            My Sessions
          </button>

          <button className="nav-item">
            <BarChart3 size={18} />
            Progress
          </button>

        </nav>

        <div className="sidebar-bottom">

          <div className="learning-card">
            <div className="learning-icon">
              <Brain size={18} />
            </div>

            <div>
              <strong>Keep thinking</strong>
              <p>
                The tutor won't give you
                the answer directly.
              </p>
            </div>
          </div>

          <button className="nav-item">
            <Settings size={18} />
            Settings
          </button>

        </div>
      </aside>

      {/* Main */}
      <main className="main">

        {/* Top bar */}
        <header className="topbar">

          <button
            className="mobile-menu"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={22} />
          </button>

          <div className="topbar-title">
            <span>
              AI Learning Environment
            </span>

            <h1>
              {selectedSubject} Tutor
            </h1>
          </div>

          <div className="subject-selector">

            <select
              value={selectedSubject}
              onChange={(e) =>
                setSelectedSubject(e.target.value)
              }
            >
              {subjects.map((subject) => (
                <option
                  key={subject}
                  value={subject}
                >
                  {subject}
                </option>
              ))}
            </select>

            <ChevronDown
              size={16}
              className="select-icon"
            />

          </div>
        </header>

        {/* Content */}
        <section className="content">

          {messages.length === 0 ? (

            /* Welcome */
            <div className="welcome">

              <div className="welcome-icon">
                <Brain size={38} />
              </div>

              <span className="eyebrow">
                SOCRATIC LEARNING
              </span>

              <h2>
                What would you like
                <br />
                to <span>understand?</span>
              </h2>

              <p>
                I won't simply give you the answer.
                I'll guide you through the reasoning
                so you can discover it yourself.
              </p>

              <div className="topic-grid">

                <button
                  className="topic-card"
                  onClick={() =>
                    setInput(
                      "Help me understand derivatives"
                    )
                  }
                >
                  <span className="topic-symbol">
                    ∫
                  </span>

                  <div>
                    <strong>Derivatives</strong>
                    <p>
                      Calculus fundamentals
                    </p>
                  </div>
                </button>

                <button
                  className="topic-card"
                  onClick={() =>
                    setInput(
                      "Help me understand Python loops"
                    )
                  }
                >
                  <span className="topic-symbol">
                    {"</>"}
                  </span>

                  <div>
                    <strong>Python Loops</strong>
                    <p>
                      Programming fundamentals
                    </p>
                  </div>
                </button>

                <button
                  className="topic-card"
                  onClick={() =>
                    setInput(
                      "Help me understand binary search"
                    )
                  }
                >
                  <span className="topic-symbol">
                    ◈
                  </span>

                  <div>
                    <strong>Binary Search</strong>
                    <p>
                      Algorithms &amp; logic
                    </p>
                  </div>
                </button>

                <button
                  className="topic-card"
                  onClick={() =>
                    setInput(
                      "Help me understand Newton's laws"
                    )
                  }
                >
                  <span className="topic-symbol">
                    F
                  </span>

                  <div>
                    <strong>Newton's Laws</strong>
                    <p>
                      Physics fundamentals
                    </p>
                  </div>
                </button>

              </div>
            </div>

          ) : (

            /* Chat */
            <div className="chat-container">

              {/* Adaptive status */}
              <div className="tutor-status">

                <div className="status-item">
                  <span className="status-label">
                    Action
                  </span>

                  <strong>
                    {tutorState.action}
                  </strong>
                </div>

                <div className="status-item">
                  <span className="status-label">
                    Hint Level
                  </span>

                  <strong>
                    {tutorState.hint_level}
                  </strong>
                </div>

                <div className="status-item">
                  <span className="status-label">
                    Attempts
                  </span>

                  <strong>
                    {tutorState.attempts}
                  </strong>
                </div>

              </div>

              {/* Solved banner */}
              {tutorState.solved && (
                <div className="solved-banner">
                  🎉 Great work! You've solved this
                  problem.
                </div>
              )}

              {/* Messages */}
              <div className="messages">

                {messages.map(
                  (message, index) => (

                    <div
                      key={index}
                      className={`message-row ${
                        message.role === "user"
                          ? "user-row"
                          : "tutor-row"
                      }`}
                    >

                      {message.role === "tutor" && (
                        <div className="avatar tutor-avatar">
                          <Brain size={18} />
                        </div>
                      )}

                      <div
                        className={`message ${
                          message.role === "user"
                            ? "user-message"
                            : "tutor-message"
                        }`}
                      >
                        {message.content}
                      </div>

                    </div>
                  )
                )}

                {/* Thinking indicator */}
                {loading && (
                  <div className="message-row tutor-row">

                    <div className="avatar tutor-avatar">
                      <Brain size={18} />
                    </div>

                    <div className="message tutor-message">
                      Thinking through your answer...
                    </div>

                  </div>
                )}

              </div>

              {/* Hint */}
              <button
                className="hint-btn"
                onClick={handleHint}
                disabled={
                  loading ||
                  tutorState.solved ||
                  tutorState.hint_level >= 3
                }
              >
                <Lightbulb size={17} />

                {tutorState.hint_level === 0
                  ? "Give me a hint"
                  : tutorState.hint_level === 1
                  ? "Give me another hint"
                  : tutorState.hint_level === 2
                  ? "Give me the final hint"
                  : "Maximum hints reached"}
              </button>

              {/* Provider status */}
              {tutorState.provider && (
                <div className="provider-status">

                  <span>
                    AI: {tutorState.provider}
                  </span>

                  {tutorState.latency_ms !== null && (
                    <span>
                      {Math.round(
                        tutorState.latency_ms
                      )}{" "}
                      ms
                    </span>
                  )}

                  {tutorState.fallback_used && (
                    <span>
                      Fallback used
                    </span>
                  )}

                </div>
              )}

            </div>
          )}

        </section>

        {/* Input */}
        <div className="input-area">

          <div className="input-wrapper">

            <textarea
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              onKeyDown={(e) => {

                if (
                  e.key === "Enter" &&
                  !e.shiftKey
                ) {
                  e.preventDefault();
                  handleSend();
                }

              }}
              placeholder={
                loading
                  ? "Tutor is thinking..."
                  : "Ask a question or explain what you're stuck on..."
              }
              rows={1}
              disabled={
                loading ||
                tutorState.solved
              }
            />

            <button
              className="send-btn"
              onClick={handleSend}
              disabled={
                loading ||
                !input.trim() ||
                tutorState.solved
              }
            >
              <Send size={19} />
            </button>

          </div>

          <p className="input-note">
            Socratic Tutor · Think first, answer second
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;