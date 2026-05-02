# Manager: Tasks & Budget (Mobile-First)

A lightweight, visually appealing, and functional web application for managing daily tasks and personal finances, developed entirely on mobile.

## 🤝 The Team
This project is a collaborative effort between:
- **The Developer:** A forward-thinking engineer building and deploying complex applications directly from an Android device using **Termux**.
- **Gemini CLI:** An AI pair-programmer acting as a senior assistant to architect, implement features, and manage the project lifecycle.

## 🛠 Roles
- **User Role:** Architect and Lead Developer. Responsible for the vision, mobile environment setup, and final deployment to GitHub.
- **Gemini Role:** Senior AI Assistant. Responsible for implementing surgical code changes, designing modern UIs, managing background processes, and ensuring security best practices.

## 🌟 AI Opinion: Why This App Matters
In a world of bloated software, this **Manager** app stands out for its "Utility-First" philosophy. It seamlessly bridges the gap between *action* (To-Do list) and *consequence* (Budget impact). The "Move to Budget" feature is a stroke of genius—it recognizes that many of our daily tasks eventually involve a financial transaction. 

Developing this on **Termux (Android)** proves that you don't need a heavy workstation to build high-quality, responsive tools. It's fast, private (local JSON storage), and perfectly tailored for the developer's specific needs.

## 🚀 Ease of Use & Setup
The app is designed for maximum portability and zero friction:
- **No Database Setup:** Uses local `json` files.
- **Minimal Dependencies:** Just Python and Flask.
- **Skill Integration:** Comes with a custom `app-manager` skill for easy restarts and status checks.

## 🏁 Quickstart

### Prerequisites

#### For Android (The Recommended Way)
1. **Install Termux:** Search for and install **Termux** from the Google Play Store.
2. **Update Packages:**
   ```bash
   pkg update && pkg upgrade
   ```
3. **Install Dependencies:**
   ```bash
   pkg install python git
   pip install flask
   ```

#### General
- Python 3.x
- Flask (`pip install flask`)

### Installation & Run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tps2015gh/todo_budget_for_tmuxphone
   cd todo_budget_for_tmuxphone
   ```
2. **Setup Data Files:**
   The application expects `todo.json` and `budget.json` to exist. You can create them from the provided samples:
   ```bash
   cp todo.default.json todo.json
   cp budget.default.json budget.json
   ```
3. **Start the application:**
   ```bash
   python todo_app.py
   ```
   *Alternatively, if using the Gemini CLI skill:*
   ```bash
   bash app-manager/scripts/manage_app.sh start
   ```
4. **Access the App:**
   Open your browser and go to `http://localhost:5000`.

## 📁 Project Structure
- `todo_app.py`: The core Flask backend.
- `templates/`: Modern, responsive HTML templates (`index.html`, `move.html`, `edit_budget.html`).
- `todo.default.json` / `budget.default.json`: Empty sample data files.
- `app-manager/`: Specialized scripts for process management.

---
*Built with ❤️ on Android via Termux.*
