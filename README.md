````markdown
# 🧠 AI Socratic Tutor

An AI-powered Socratic learning assistant designed to help students think through problems instead of simply receiving direct answers.

The system evaluates the student's understanding, provides adaptive Socratic guidance, and progressively increases hints when the student needs additional help.

This project is a **standalone working prototype developed for a hackathon**.

---

# 📌 Features

- 🧠 Socratic AI tutoring
- 💡 Progressive hint system
- 📊 Student understanding evaluation
- 🎯 Adaptive decision engine
- 🔄 Multiple AI providers
- 🛟 Automatic provider fallback
- ⚡ Provider latency tracking
- 📚 Subject selection
- 💬 Conversation history
- 🆕 New tutoring sessions
- 📱 Responsive React interface
- 🔐 API keys stored securely on the backend

---

# 🏗️ Project Architecture

```text
Student
   │
   ▼
React Frontend
   │
   │ HTTP / JSON
   ▼
FastAPI Backend
   │
   ▼
Tutor Service
   │
   ▼
Decision Engine
   │
   ▼
Fallback Tutor Service
   │
   ├───────────────┐
   ▼               ▼
Gemini            Groq
Primary           Fallback
````

---

# 📁 Project Structure

```text
ai-socratic-tutor/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── tutor.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── tutor_service.py
│   │       ├── fallback_service.py
│   │       ├── decision_engine.py
│   │       ├── provider_result.py
│   │       ├── schemas.py
│   │       │
│   │       └── providers/
│   │           ├── __init__.py
│   │           ├── base.py
│   │           ├── gemini_provider.py
│   │           └── groq_provider.py
│   │
│   ├── .env
│   ├── requirements.txt
│   └── venv/
│
├── frontend/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   │
│   │   └── api/
│   │       └── tutorApi.js
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── .gitignore
└── README.md
```

---

# 💻 Running the Project Locally

## 1. Prerequisites

Before running the project, install:

* Git
* Python 3.11 or later
* Node.js 18 or later
* npm

Check your installed versions:

```bash
git --version
python --version
node --version
npm --version
```

Recommended development versions:

```text
Python 3.11+
Node.js 22+
npm 10+
```

---

# 📥 Download the Project from GitHub

## Option 1 — Clone using Git

Open a terminal or Command Prompt.

Run:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Then enter the project:

```bash
cd ai-socratic-tutor
```

> Replace `YOUR_USERNAME/YOUR_REPOSITORY` with the actual GitHub repository path.

---

## Option 2 — Download ZIP

If Git is not installed:

1. Open the GitHub repository.
2. Click **Code**.
3. Click **Download ZIP**.
4. Extract the ZIP file.
5. Open the extracted `ai-socratic-tutor` folder in VS Code.

---

# 🐍 Backend Setup

Open a terminal inside the project folder.

Navigate to the backend:

```bash
cd backend
```

---

## 2. Create a Python Virtual Environment

Run:

```bash
python -m venv venv
```

### Windows

Activate the virtual environment:

```bash
venv\Scripts\activate
```

After activation, the terminal should show something similar to:

```text
(venv) C:\...\ai-socratic-tutor\backend>
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

# 📦 3. Install Backend Dependencies

Run:

```bash
pip install -r requirements.txt
```

This installs the required Python packages including the FastAPI server and AI provider libraries.

---

# 🔑 4. Configure API Keys

Inside the `backend` folder, create a file named:

```text
.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key

TUTOR_PRIMARY_PROVIDER=gemini
TUTOR_FALLBACK_PROVIDER=groq
```

Replace:

```text
your_gemini_api_key
```

and

```text
your_groq_api_key
```

with your actual API keys.

### Important

Never upload your `.env` file to GitHub.

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
node_modules/
dist/
```

---

# ▶️ 5. Start the Backend

Make sure you are inside:

```text
backend/
```

and that the virtual environment is activated.

Run:

```bash
uvicorn app.main:app --reload
```

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

The backend is now running at:

```text
http://localhost:8000
```

---

# 🧪 6. Test the Backend

Open your browser and visit:

```text
http://localhost:8000/docs
```

FastAPI will display the interactive API documentation.

Find:

```text
POST /api/tutor/chat
```

You can use the **Try it out** button to test the tutor API.

---

# ⚛️ Frontend Setup

Open a **new terminal**.

Do not close the backend terminal.

From the project root:

```bash
cd frontend
```

---

# 📦 7. Install Frontend Dependencies

Run:

```bash
npm install
```

This installs all dependencies listed in:

```text
frontend/package.json
```

---

# ▶️ 8. Start the Frontend

Run:

```bash
npm run dev
```

Vite will display a URL similar to:

```text
Local: http://localhost:5173/
```

Open:

```text
http://localhost:5173
```

in your browser.

---

# 🚀 Complete Local Setup

You need **two terminals** running simultaneously.

## Terminal 1 — Backend

```bash
cd ai-socratic-tutor/backend
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Then:

```bash
uvicorn app.main:app --reload
```

---

## Terminal 2 — Frontend

```bash
cd ai-socratic-tutor/frontend
```

Then:

```bash
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🔄 Application Flow

Once both servers are running:

```text
Browser
   │
   │ http://localhost:5173
   ▼
React Frontend
   │
   │ POST /api/tutor/chat
   ▼
FastAPI Backend
   │
   ▼
Tutor Service
   │
   ▼
Decision Engine
   │
   ▼
AI Provider
   │
   ├── Gemini
   │
   └── Groq fallback
   │
   ▼
Tutor Response
   │
   ▼
React UI
```

---

# 💬 Example Usage

Select a subject:

```text
Computer Science
```

Ask:

```text
I don't understand binary search.
```

The tutor should guide you rather than immediately providing the complete answer.

For example:

```text
Tutor:

Think about the fact that the array is sorted.

If you had 100 elements, would checking them
one by one be the most efficient approach?
```

The student can then respond and continue the conversation.

---

# 💡 Hint System

When the student needs additional help, click:

```text
Give me a hint
```

The system progressively increases the hint level:

```text
Hint Level 0
     ↓
Hint Level 1
     ↓
Hint Level 2
     ↓
Hint Level 3
```

The tutor attempts to provide stronger guidance without immediately revealing the complete solution.

---

# 🔄 AI Provider Fallback

The project supports two AI providers.

Default configuration:

```env
TUTOR_PRIMARY_PROVIDER=gemini
TUTOR_FALLBACK_PROVIDER=groq
```

If Gemini encounters a supported failure such as:

```text
401 Authentication Error
429 Rate Limit
Quota Exhausted
Timeout
503 Service Unavailable
```

the fallback service attempts to use Groq.

Example backend output:

```text
Primary provider gemini failed: 429 RESOURCE_EXHAUSTED

Provider: groq
Latency: 850.21 ms
Fallback: True
```

This makes the prototype more reliable during demonstrations.

---

# 📡 API Endpoint

## `POST /api/tutor/chat`

### Request

```json
{
  "message": "Explain binary search",
  "history": [],
  "hint_level": 0,
  "session_id": "example-session",
  "subject": "Computer Science"
}
```

### Response

```json
{
  "message": "What do you notice about the middle element?",
  "stage": "guiding",
  "action": "ask_question",
  "hint_level": 0,
  "student_understanding": "beginner",
  "answer_evaluation": "needs_guidance",
  "confidence": 0.82,
  "should_reveal_answer": false,
  "provider": "gemini",
  "fallback_used": false,
  "latency_ms": 1250
}
```

---

# 🛠️ Troubleshooting

## Backend does not start

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'groq'
```

Run:

```bash
pip install -r requirements.txt
```

or:

```bash
pip install groq
```

---

## Frontend dependencies missing

Run:

```bash
cd frontend
npm install
```

Then:

```bash
npm run dev
```

---

## Frontend cannot connect to backend

Make sure the backend is running:

```bash
uvicorn app.main:app --reload
```

Then check:

```text
http://localhost:8000/docs
```

If the FastAPI documentation opens, the backend is running.

---

## Gemini quota exceeded

You may see:

```text
429 RESOURCE_EXHAUSTED
```

The application is designed to use the fallback provider when supported.

You can also switch the providers in `.env`:

```env
TUTOR_PRIMARY_PROVIDER=groq
TUTOR_FALLBACK_PROVIDER=gemini
```

Restart the backend after changing `.env`.

---

## Port already in use

If port `8000` is already being used:

```bash
uvicorn app.main:app --reload --port 8001
```

If you do this, update the frontend API URL from:

```text
http://localhost:8000
```

to:

```text
http://localhost:8001
```

---

# 🔐 Security Notes

Never commit:

```text
.env
```

to GitHub.

Never place AI API keys directly inside:

```text
App.jsx
tutorApi.js
```

or any other frontend file.

The correct architecture is:

```text
React
  ↓
FastAPI
  ↓
Environment Variables
  ↓
AI Provider
```

---

# 🏆 Hackathon Demonstration

Recommended demonstration:

### 1. Start the application

```bash
uvicorn app.main:app --reload
```

and:

```bash
npm run dev
```

### 2. Open the tutor

```text
http://localhost:5173
```

### 3. Select a subject

Example:

```text
Mathematics
```

### 4. Ask a problem

```text
I don't understand derivatives.
```

### 5. Show Socratic guidance

Demonstrate that the AI does not immediately reveal the answer.

### 6. Give a student attempt

```text
I think a derivative tells us the value of a function.
```

### 7. Request a hint

Click:

```text
Give me a hint
```

### 8. Demonstrate progressive hints

Show:

```text
Hint 1
→ Hint 2
→ Hint 3
```

### 9. Demonstrate fallback

If possible, temporarily simulate or use a provider failure and show:

```text
Gemini failed
      ↓
Groq activated
      ↓
Tutor continues working
```

This demonstrates one of the stronger technical aspects of the project.

---

# 🎯 Project Goal

The goal is not to build another AI chatbot.

The goal is to create an AI tutor that encourages:

```text
Think
  ↓
Attempt
  ↓
Understand
  ↓
Receive Guidance
  ↓
Try Again
  ↓
Solve
```

rather than:

```text
Question
  ↓
AI
  ↓
Answer
```

---

# 🔮 Future Improvements

Planned improvements include:

* Student authentication
* Persistent tutoring sessions
* Progress dashboard
* Learning analytics
* RAG-based educational resources
* PDF/course-material support
* Automatic topic detection
* Misconception tracking
* Personalized learning paths
* Additional AI providers
* Database integration

---

# 📜 Development Status

This is a **working hackathon prototype** and is actively under development.

Some features described in the future improvements section are planned but are not currently implemented.

---

# 👨‍💻 Local Development Summary

For a quick setup:

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# Enter project
cd ai-socratic-tutor

# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Create .env and add API keys

# Start backend
uvicorn app.main:app --reload
```

Open another terminal:

```bash
# Frontend
cd ai-socratic-tutor/frontend

npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

Backend API documentation:

```text
http://localhost:8000/docs
```

---

# ⭐ Quick Start

```text
1. Clone GitHub repository
        ↓
2. Configure backend/.env
        ↓
3. Create Python virtual environment
        ↓
4. pip install -r requirements.txt
        ↓
5. Start FastAPI
        ↓
6. npm install
        ↓
7. npm run dev
        ↓
8. Open localhost:5173
        ↓
9. Start learning 🚀
```

````

### One important GitHub note
make sure your repository contains:

```text
requirements.txt
package.json
.gitignore
README.md
````

but **does NOT contain**:

```text
backend/.env
backend/venv/
frontend/node_modules/
```

And in the README, replace:

```text
https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

with your **actual GitHub repository URL** before pushing it.
