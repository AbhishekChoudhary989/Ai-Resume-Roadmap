# 🚀 AI Resume & Career Architect

A full-stack AI application that analyzes resumes to provide personalized career roadmaps, skill gap assessments, and professional profiling.


## 🌟 Features

* **📄 PDF Resume Parsing:** Extracts text safely from PDF documents.
* **🤖 AI-Powered Analysis:** Uses Google Gemini to act as a "Senior Technical Recruiter".
* **🛡️ Smart Document Validation:** Automatically rejects non-resume files (like bills, source code, government forms, or log files) before processing.
* **🗺️ Career Roadmap:** Generates a structured 6-month plan to bridge skill gaps.
* **✨ Modern UI:** Built with Next.js, Framer Motion animations, and Markdown rendering.

---

## 🛠️ Tech Stack

### Frontend (Client)
* **Framework:** Next.js / React
* **Styling:** Tailwind CSS (implied), Lucide React (Icons)
* **Animations:** Framer Motion
* **HTTP Client:** Axios
* **Rendering:** React Markdown (with GFM)

### Backend (Server)
* **Framework:** Python Flask
* **AI Model:** Google Gemini (via API)
* **PDF Processing:** PyPDF2 / PDFMiner (implied)
* **CORS:** Flask-CORS for secure frontend-backend communication

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Ai-Resume-Roadmap.git](https://github.com/YOUR_USERNAME/Ai-Resume-Roadmap.git)
cd Ai-Resume-Roadmap

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

GOOGLE_API_KEY=your_actual_api_key_here

cd client

# Install Node modules
npm install

# Run the development server
npm run dev

📖 How to Use
Open the application in your browser.

Click "Drop your PDF here" to select a resume.

Click "Analyze My Career".

Wait for the AI to validate and process the document.

View your Professional Profile, Skill Gaps, and Career Roadmap displayed below.

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.
