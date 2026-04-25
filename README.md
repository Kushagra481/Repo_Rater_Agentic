# 🤖 RepoAgent Lite — Multi-Agent GitHub Repository Analyzer

RepoAgent Lite is a **multi-agent AI system** that analyzes GitHub repositories and generates structured improvement reports with actionable suggestions.

It uses a **branching agent architecture (LangGraph)** where multiple specialized agents independently evaluate different aspects of a repository and then merge their reasoning into a final decision.

---

## 🚀 Live Demo

👉 [*Add your Streamlit link here after deployment*](https://reporateragentic-yrubwdcudwsvqhpqufrjdv.streamlit.app/)

---

## 🧠 Key Idea

Instead of a single linear pipeline, RepoAgent Lite uses **parallel reasoning agents**:

```txt
            ┌───────────────┐
            │ Scanner Agent │
            └──────┬────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │              │
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────────┐
│Structure│  │ Docs    │  │ Code    │  │ Security   │
│ Agent   │  │ Agent   │  │ Agent   │  │ Agent      │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬──────┘
     └────────────┴────────────┴────────────┘
                    │
             ┌────────────┐
             │ Merge Agent│
             └────┬───────┘
                  │
          ┌──────────────┐
          │ Planner Agent│
          └────┬─────────┘
               │
        ┌──────────────┐
        │ Reporter     │
        └──────────────┘
```

---

## ✨ Features

* 🔍 **Repository Scanning**

  * Clones repo and builds file tree
  * Extracts key files (README, requirements, LICENSE, etc.)

* 🧠 **Multi-Agent Reasoning**

  * Structure Agent → project layout
  * Docs Agent → README quality
  * Code Agent → code health & size
  * Security Agent → secret detection

* 📊 **Scoring System**

  * Each agent produces a score
  * Final merged score out of 100

* 🛠 **Automated Issue Generation**

  * GitHub-style issues
  * Prioritized suggestions

* 📄 **Markdown Report Export**

  * Full analysis downloadable

---

## 🏗 Tech Stack

* Python
* Streamlit
* LangGraph (multi-agent workflow)
* GitPython
* Pandas

---

## 📂 Project Structure

```txt
Repo_Agentic/
│── app.py
│── requirements.txt
│── README.md
│
├── agents/
│   ├── scanner_agent.py
│   ├── structure_agent.py
│   ├── docs_agent.py
│   ├── code_agent.py
│   ├── security_agent.py
│   ├── merge_agent.py
│   ├── planner_agent.py
│   └── reporter_agent.py
│
├── tools/
│   ├── repo_loader.py
│   └── file_tree.py
```

---

## ⚙️ Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/Repo_Rater_Agentic.git
cd Repo_Rater_Agentic

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
streamlit run app.py
```

---

## 🐳 Docker (Optional)

```bash
docker compose up --build
```

---

## 🧪 Example Output

The system generates:

* Repository summary
* File tree
* Multi-agent scores
* Weaknesses & strengths
* Improvement recommendations
* GitHub-style issues

---

## 📌 Future Improvements

* LLM-powered reasoning layer (hybrid agent system)
* GitHub PR auto-review bot
* Code complexity analysis
* Test coverage detection
* Architecture diagram generation

---

## 💡 Use Cases

* Open-source contribution planning
* Codebase onboarding
* Repo quality auditing
* Developer productivity tools

---

## 👨‍💻 Author

Kushagra Shukla

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
