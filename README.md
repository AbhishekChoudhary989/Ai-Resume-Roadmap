# 🏛️ Career Architect AI 

**Career Architect AI** is a high-end career trajectory mapping tool. It uses Artificial Intelligence to analyze resumes, identify critical skill gaps, and provide a 6-month actionable roadmap benchmarked against live job market data from India.

---

## ✨ Key Features
- **Intelligent Resume Parsing**: Extracts text from PDFs using `PyMuPDF` and `pypdf`.
- **AI Roadmap Generation**: Powered by **Google Gemini 2.5 Flash** to create personalized career blueprints.
- **Live Market Benchmarking**: Scrapes real-time job listings from **Indeed India** using the Apify SDK.
- **Skill Gap Measurement**: Compares your current profile against market demands to highlight missing competencies.
- **Cyber-Pulse Dashboard**: A modern, animated UI built with **Next.js 15**, **Tailwind CSS**, and **Framer Motion**.
- **Interactive Loading State**: Immersive Lottie animations to engage users during data processing.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Styling**: Tailwind CSS (Glassmorphism design)
- **Animations**: Framer Motion & Lottie Files
- **Icons**: Lucide React

### Backend
- **Framework**: Flask (Python)
- **AI Model**: Google Gemini 2.5 Flash API
- **Scraper**: Apify Indeed Scraper
- **PDF Engine**: PyMuPDF / pypdf

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.10+**
- **Node.js (LTS)**
- **Git**

### 2. Clone the Repository
bash
git clone [https://github.com/AbhishekChoudhary989/Ai-Resume-Roadmap.git](https://github.com/AbhishekChoudhary989/Ai-Resume-Roadmap.git)
cd Ai-Resume-Roadmap


3. Backend Setup
Bash

# Install dependencies
```pip install flask flask-cors python-dotenv pypdf google-genai apify-client tenacity pymupdf```
4. Frontend Setup
Bash

cd client
# Install dependencies
npm install
5. Environment Variables
Create a .env file in the root directory and add your API keys:

Code snippet

GOOGLE_API_KEY=your_gemini_api_key
APIFY_API_TOKEN=your_apify_token
🏃 Running the Application
You need two terminals running simultaneously:

Terminal 1 (Backend):

Bash

python backend.py
Terminal 2 (Frontend):

Bash

cd client
npm run dev
The application will be live at http://localhost:3000.

🛡️ License
This project is for educational purposes as part of a portfolio project.

🤝 Contributing
Feel free to fork this repository and submit pull requests for any features or UI improvements!


---

### **How to add this to GitHub:**
1. Save the text above into a file named **`README.md`** inside your `JobApp` folder.
2. Open your terminal and run:
   ```bash
   git add README.md
   git commit -m "Added detailed README documentation"
   git push origin main
