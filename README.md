# 🤖 Project Codexa  
**Unlock your future, in your language.**

Project Codexa is a complete, offline-first AI learning platform designed to shatter the educational barriers faced by students in rural and underserved communities. It transforms a basic laptop into a personal, multilingual tutor that runs 100% offline, providing a patient and adaptive learning companion for every student, anywhere.

---

## ✨ Key Features
- **100% Offline AI Tutor**  
  A multi-subject expert in Math, Sciences, English, and Coding that runs entirely on the user's machine.  

- **Adaptive Bilingual Support**  
  The tutor defaults to English but intelligently detects and switches to a student's native Indian language (like Telugu or Malayalam) to ensure concepts are clearly understood.  

- **Socratic Teaching Method**  
  It's not an answer machine; it's a real teacher. The AI guides students with open-ended questions to foster critical thinking.  

- **Smart, Proactive Quizzing**  
  The AI generates interactive quizzes after a concept is explained, with a persistent "card" layout that allows students to review their answers.  

- **Polished User Experience**  
  A clean, professional interface with a "thinking" animation, celebratory balloons for correct answers, and a helpful sidebar for quick actions.  

---

## 🚀 How It Works
**Project Codexa** is a full-stack, offline application built with a focus on accessibility and performance.  

- **AI Backend**  
  Uses **Ollama** to run powerful open-source Large Language Models (**Mistral-7B**, **gpt-oss:20b**) locally, with GPU acceleration enabled for optimal performance.  

- **The Tutor’s "Brain"**  
  A sophisticated **SYSTEM_PROMPT** engineered with a strict, mode-based system that defines the tutor's personality, bilingual capabilities, Socratic teaching style, and structured quiz-generation format.  

- **Frontend Interface**  
  A clean, interactive application built with **Streamlit**.  

---

## 🛠️ Getting Started

### Prerequisites
- Python **3.8+**  
- **Ollama** installed and running on your system  
- An **NVIDIA GPU** is recommended for best performance  

### Installation

Clone the repository:
```bash
git clone https://github.com/your-username/project-codexa.git
cd project-codexa
```
Create and activate a virtual environment:
```bash
python -m venv venv
```
# On Windows
```bash
.\venv\Scripts\activate
```
# On macOS/Linux
```bash
source venv/bin/activate
```
# Install the required libraries:
```bash
pip install -r requirements.txt
```
Pull the AI Model (recommended):
```bash
ollama pull gpt-oss:20b
```
# Running the Application

Make sure your Ollama server is running.
In your activated terminal, run:
```bash
streamlit run app.py
```
## 🔮 Future Roadmap

This project is a powerful prototype with a clear path forward. Our future vision includes:

Local Database & Dashboard
Implementing a SQLite database to track long-term student progress and display it in a data-driven dashboard.

Gamification
Adding streaks, badges, and points to make learning even more engaging.

Mobile Version
Developing a standalone mobile application using a highly optimized model like phi3:mini.

