````markdown
# 🔢 Battle of Numbers – Multiplayer Strategy Game

A web-based two-player number strategy game built using Django. Players take turns applying numbers and mathematical operations to manipulate scores strategically.

---

## 🎮 Game Rules

- Each player starts with a unique list of numbers.
- Players can apply an operand (`+`, `-`, `*`, `/`) to the opponent's score using one of their available numbers.
- Once a number is used, it and all smaller numbers are removed.
- Each operand can be used **only once**.
- When a player exhausts all their numbers, the other player continues until they too run out or the round limit is reached.
- The player with the **higher score** at the end wins.

---

## 🛠 Tech Stack

- **Backend**: Django (Python 3.x)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default with Django)

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/number-game.git
   cd number-game
````

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the server**

   ```bash
   python manage.py runserver
   ```

6. **Access the game**
   Open `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```
numbergame/
├── game/               # Game app (views, models, templates)
│   ├── templates/
│   │   └── game/
│   │       ├── play.html
│   │       └── winner.html
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── custom_tags.py
├── numbergame/         # Project settings
│   ├── settings.py
│   └── urls.py
├── static/             # Static assets (if any)
├── db.sqlite3
└── manage.py
```

---

## 🧪 Features in Progress

* Multiplayer game via shareable link.
* Auto round tracking and end-game logic.
* Operands usage tracking with color-coded UI.
* Cool animations and responsiveness.

---

## 🧠 Future Enhancements

* Live multiplayer with WebSockets.
* Timer-based turns.
* Player login system.
* Game replays and leaderboards.

---

## 🤝 Contributing

PRs and suggestions are welcome! Fork this repo, make changes, and submit a pull request 🚀

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
