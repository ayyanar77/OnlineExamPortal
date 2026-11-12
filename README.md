# 🎓 EpicalExam — Smart Online Examination Portal

**EpicalExam** is a modern, lightweight, full-stack web application built with **Python (Flask)** and a **Glassmorphic Dark UI**. It provides an end-to-end examination platform with candidate registration, secure authentication, student dashboards, proctored anti-cheat examination environments, automated real-time grading, and comprehensive performance analytics.

---

## 🚀 Key Features

### 1. Candidate Registration & Authentication
- **Multi-step Onboarding**: Guided 3-step registration capturing Personal, Academic, and Security details.
- **Form Validation**: Real-time client-side checks and server-side regex validations for email, roll number, and password complexity.
- **Secure Password Hashing**: Passwords stored using SHA-256 cryptography.
- **Session Management**: Protected routes requiring active user authentication.

### 2. Candidate Dashboard
- **Live Performance Counters**: Tracks total exams attempted, average score %, and tests passed.
- **Subject Catalogs**: Searchable and filterable list of all available and upcoming examinations.
- **Candidate Profile**: Displays academic details, enrollment year, roll number, and institution.
- **Upcoming Schedule**: View examination dates and test timings.

### 3. Proctored & Anti-Cheat Examination Engine
- **Tab-Switch Detection**: Monitors window focus (`visibilitychange`, `window.blur`) and logs any tab switches directly to the candidate's exam report.
- **Input Lockdown**: Disables right-click context menus, copy/cut/paste, and inspection hotkeys (`F12`, `Ctrl+U`, `Ctrl+C`, etc.).
- **Countdown Timer**: Real-time timer with urgent color alerts and automatic test submission upon expiration.
- **Question Palette**: Color-coded question navigator (Answered, Unanswered, Current).
- **Session Resilience**: Temporary browser caching ensures progress is not lost upon accidental reloads.

### 4. Automated Grading & Detailed Performance Analytics
- **Server-Side Verification**: Question responses are graded securely on the backend against protected answer keys.
- **Instant Result Generation**: Computes total score, percentage, pass/fail status, and time taken.
- **Question-by-Question Review**: Visual breakdown showing candidate selections versus correct answers.
- **Printable Reports**: Built-in support to save or print official examination scorecards.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Backend** | Python 3, Flask | Routing, authentication, grading logic, session handling |
| **Frontend** | HTML5, CSS3, JavaScript (ES6) | Responsive, glassmorphic dark theme, particle animations |
| **Icons & Typography** | FontAwesome 6, Google Fonts (Outfit) | Modern UI styling |
| **Data Storage** | JSON Flat-File Database | Lightweight, portable persistent storage (`candidates.json`, `exams.json`, `results.json`) |

---

## 📂 Project Structure

```
d:\EpicalExam\
│
├── app.py                     # Main Flask application and backend routes
├── candidates.json            # Candidate accounts data store
├── exams.json                 # Question bank and exam modules
├── results.json               # Recorded student scores and proctoring audit logs
├── README.md                  # Project documentation
│
├── static/
│   ├── css/
│   │   ├── register.css       # Styles for candidate registration
│   │   ├── login.css          # Styles for sign-in page
│   │   └── dashboard.css      # Styles for candidate dashboard & palettes
│   └── js/
│       ├── register.js        # Multi-step validation & password strength meter
│       ├── login.js           # Login form handler & validation
│       └── dashboard.js       # Sidebar toggles, tab navigation, & counters
│
├── templates/
│   ├── register.html          # Registration form template
│   ├── login.html             # Sign-in portal template
│   ├── dashboard.html         # Candidate overview, exam catalog, & results
│   ├── exam.html              # Proctored live examination interface
│   └── result.html            # Detailed test score report & question review
│
└── EpicalExam\venv\           # Python virtual environment
```

---

## 📋 Available Exam Modules

| Module Name | Subject | Questions | Duration | Pass Mark |
|---|---|:---:|:---:|:---:|
| **Python Programming** | Computer Science | 10 | 15 mins | 60% |
| **Data Structures & Algorithms** | Computer Science | 10 | 20 mins | 60% |
| **Web Development** | Information Technology | 10 | 15 mins | 60% |
| **SQL & Database Management** | Information Technology | 10 | 15 mins | 60% |
| **Computer Networks** | Computer Science | 10 | 15 mins | 60% |

---

## 🚦 Getting Started

### Prerequisites
- Python 3.8+ installed on your system
- PowerShell or Command Prompt

### Step 1: Clone or Navigate to the Project Directory
```powershell
cd d:\EpicalExam
```

### Step 2: Activate the Virtual Environment
```powershell
.\EpicalExam\venv\Scripts\Activate.ps1
```
*(If prompted by execution policy on Windows PowerShell, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install Required Dependencies
```powershell
pip install flask
```

### Step 4: Run the Application
```powershell
python app.py
```
*Alternatively, run directly with the virtualenv binary:*
```powershell
.\EpicalExam\venv\Scripts\python.exe app.py
```

### Step 5: Access the Web Application
Open your web browser and visit:
👉 **`http://127.0.0.1:5000`**

---

## 🧭 Application Workflow

1. **Register**: Go to `/register`, complete the 3-step personal and academic profile, and set a password.
2. **Sign In**: Go to `/login` and authenticate with your registered email and password.
3. **Dashboard**: Navigate to `/dashboard` to view your profile, statistics, and available tests.
4. **Take Exam**: Click **"Start Exam Now"** under **My Exams** (`/exam/<id>`).
5. **Proctored Session**: Answer the multiple-choice questions while adhering to fullscreen and anti-cheat policies.
6. **Submit & Review**: Submit your test (`/exam/<id>/submit`) to instantly view your graded scorecard (`/result/<id>`).

---

## 🔒 Security Highlights

- **Anti-Tampering**: Answer keys are never sent to the client browser during the exam; grading is strictly server-side.
- **Repeat Prevention**: Once an exam is completed by a student, re-attempts are blocked to preserve test integrity.
- **Proctoring Audit**: Any tab-switching or minimization incidents are counted and permanently attached to the student's submission record.

