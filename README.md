#  ReviewIQ – AI-Powered Code Review & Learning Assistant

ReviewIQ is a full-stack AI-powered code review platform that allows developers to submit code, receive structured AI-generated reviews, and interact with a context-aware assistant to understand bugs, improve code quality, and learn from mistakes.

The platform is designed to go beyond static code analysis by providing an interactive, session-based review experience similar to ChatGPT, but focused specifically on code understanding and improvement.

---

##  Live Demo

🔗 **Frontend:** https://reviewiq-ai.lovable.app

🔗 **Backend API:** https://reviewiq-m3c5.onrender.com/docs

---

#  Problem Statement

Modern developers rely on static analysis tools, linters, and IDE diagnostics to identify issues in their code. While these tools are effective at detecting syntax and basic logical errors, they provide limited contextual understanding of *why* an issue exists and *how* to systematically fix it.

As a result:

-  Code feedback is often fragmented and tool-specific rather than unified and structured.
-  Developers lack an interactive way to explore reasoning behind bugs.
-  Learning from mistakes is not reinforced through contextual explanations.
-  Debugging remains a manual, repetitive process across different codebases.

> Existing tools focus primarily on **detection** rather than **explanation and learning-oriented feedback**.

---

##  Solution

ReviewIQ solves this by providing an AI-driven code review system where:

-  Users submit code snippets.
-  The system generates structured AI-based reviews.
-  Users can ask follow-up questions about the same code submission.
-  Each submission becomes a persistent learning session.

This transforms code review from a one-time check into an interactive learning experience.

---

##  Key Features

###  AI-Powered Code Review
Users receive structured feedback including:
-  Bug detection
-  Severity classification (Critical / Major / Minor)
-  Code improvement suggestions
-  High-level summary of code quality

###  Context-Aware Chat System
Users can ask follow-up questions such as:
- "Why is this bug important?"
- "How do I fix this properly?"
- "Explain line 10 of my code"

All responses are tied to the same submission context.

###  Session-Based Architecture
Each code submission is treated as an independent review session.
-  New code → new submission
-  Chat stays bound to that submission
-  No context mixing between different reviews

###  Code Submission System
Users can:
- Paste code
- Select programming language
- Submit for AI analysis

###  Review History
Users can revisit all previous submissions with full review details and chat history.

###  Dashboard Analytics
Provides insights such as:
-  Total reviews generated
-  Total bugs detected
-  Critical bug count
-  Language distribution
-  Recent activity

---

##  System Architecture

```
User Browser
        ↓
React Frontend
        ↓
Node.js / Express Backend
        ↓
AI Review Engine (LLM-based processing)
        ↓
Database (PostgreSQL / MongoDB)
        ↓
Structured Review + Chat Responses
        ↓
Frontend Rendering (Dashboard + Workspace UI)
```

---

##  Request Flow

```
User submits code
        ↓
Frontend sends request to backend
        ↓
Backend creates new submission record
        ↓
AI engine analyzes code
        ↓
Structured review is generated:
    - Bugs
    - Summary
    - Suggestions
        ↓
Response stored with submission_id
        ↓
User opens review workspace
        ↓
User asks follow-up questions
        ↓
Chat API responds using same submission context
```
---

## Tech Stack

### Backend
- Node.js / Express
- REST API architecture
- AI integration layer (LLM-based analysis)
- Session-based submission handling
- Context-aware chat system

### Frontend
- React (Vite)
- React Router / TanStack Router
- Code editor interface
- Review workspace UI
- Chat system per submission

### Database
- PostgreSQL / MongoDB
- Stores:
  - Users
  - Submissions
  - Reviews
  - Chat history

### AI Layer
- Groq LLaMA 3.3 70B
- Prompt-engineered structured outputs
- JSON-based response formatting

### Deployment
- Frontend: Lovable
- Backend: Render
- Database: PostgreSQL

---

##  Challenges Faced

### 1. Frontend Deployment & Routing Issues

Deploying the frontend in production was challenging due to routing conflicts and 404 errors when navigating directly to nested routes. While the application worked correctly in development, production environments required proper client-side routing configuration and deployment adjustments.

Tools like Lovable were used for initial UI generation, but integrating and deploying a standalone production build introduced inconsistencies across environments.

### 2. AI Prompt Engineering & Structured Output Control

One of the major challenges was designing prompts that consistently generate structured and reliable AI responses for code reviews. The system required strict JSON formatting for:

- bug detection
- severity classification
- summaries
- suggestions

Iterative prompt refinement was required to ensure stable output formatting and reduce parsing failures across different code inputs.

### 3. Session-Based Context Management

Implementing session-based architecture required ensuring that each code submission maintains an isolated context. The system had to differentiate between:

- chat queries within an existing submission
- new code submissions creating a new session

This was critical to prevent context mixing and maintain accurate, submission-specific AI responses throughout the workflow.

---

## Key Learning Outcomes

- Building session-based AI applications
- Designing RESTful APIs
- Integrating LLMs into real systems
- Context-aware chat systems
- Full-stack SaaS deployment
- React production routing handling
- Scalable backend architecture design

---

## Future Improvements

- GitHub PR integration
- Team collaboration features
- AI-powered refactoring suggestions
- Inline code annotations
- Performance benchmarking

---

## Author

**Geethika Tammineni**

Aspiring Software Engineer | Backend Development | AI Systems

Focused on building real-world AI applications that improve developer productivity through intelligent automation and structured feedback systems.

