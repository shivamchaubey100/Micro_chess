## 🧠 Microchess Agents — IIT Bombay CS747 Assignment

### Overview

This repository contains three intelligent agents developed for the **Microchess** environment as part of the **CS747: Foundations of Intelligent and Learning Agents** course at **IIT Bombay**.

Each agent is designed to play progressively stronger chess games on a **5×4 Microchess board**, using increasingly sophisticated search and evaluation techniques — from simple heuristics to optimized alpha-beta search.

---

## 📁 Project Structure

```
├── agents/
│   ├── base_agent.py
│   ├── random.py
│   ├── task1_agent.py
│   ├── task2_agent.py
│   └── task3_agent.py
├── minichess/
│   └── chess/
│       ├── fastchess.py
│       └── fastchess_utils.py
├── autograder.py
├── README.md
└── report.tex
```

---

## ⚙️ Agents Overview

### **Task 1 — Heuristic-Based 2-Ply Agent**

A fast rule-based agent that uses:

* Simple **material evaluation** (piece values only)
* Shallow **2-ply minimax search**
* Lightweight pruning and move ordering
* Designed to outperform the Random Agent under **5 ms per move**

**Key result:**
✅ 40 wins vs RandomAgent (Task-1 Passed)

---

### **Task 2 — Shallow Alpha-Beta Agent**

Introduces search optimizations and positional heuristics:

* **Alpha-beta pruning** for efficient minimax search
* **Pawn advancement** and **center control** in evaluation
* **Selective deepening** on tactical moves
* **Move ordering** prioritizing captures and promotions

**Key result:**
✅ 48 wins vs RationalAgent (Task-2 Passed)

---

### **Task 3 — Optimized Negamax with Heuristics**

A high-performance agent implementing:

* **Negamax alpha-beta search** with selective extensions
* **MVV/LVA move ordering** and **killer moves**
* **Tuned evaluation function** including:

  * Material
  * Pawn pressure
  * Center control
  * Mobility bonus
* Efficient pruning and adaptive depth control for time compliance

**Key result:**
✅ 66 wins vs RationalAgent (Task-3 Passed under 0.2 s/move)

---

## 🧩 Evaluation Functions Summary

| Term             | Description                                     | Used In    |
| ---------------- | ----------------------------------------------- | ---------- |
| Material         | Weighted sum of piece values                    | All agents |
| Pawn Advancement | Reward for forward pawn progress                | Task 2 & 3 |
| Center Control   | Encourages central piece activity               | Task 2 & 3 |
| Mobility         | Number of legal moves                           | Task 3     |
| Blunder Penalty  | Penalizes positions with immediate capture risk | Task 3     |

---

## 🧠 Algorithms Implemented

* **Task 1:** 2-ply Minimax (material heuristic)
* **Task 2:** 3-ply Alpha-Beta with heuristic ordering
* **Task 3:** Negamax with Alpha-Beta pruning, extensions, and move heuristics

All agents were benchmarked using the provided `autograder.py` with strict time limits:

| Task | Opponent      | Avg Move Time | Score | Status   |
| ---- | ------------- | ------------- | ----- | -------- |
| 1    | RandomAgent   | 0.002–0.005 s | 65–70 | ✅ Passed |
| 2    | RationalAgent | 0.04 s        | 57    | ✅ Passed |
| 3    | RationalAgent | 0.16–0.18 s   | 60–63 | ✅ Passed |

---

## 🚀 Running the Project

### Prerequisites

* Python==3.9.6
* chess==1.9.3
* numpy==1.23.3
* numba==0.56.2
* pygame==2.6.1
* tqdm==4.64.1
* FastChess environment provided in `minichess/`

### Run Autograder

```bash
python3 autograder.py --task 1
python3 autograder.py --task 2
python3 autograder.py --task 3
```

### Example Output

```
=== FINAL RESULTS ===
Task3Agent:
  Wins as White: 42
  Wins as Black: 23
  Total Wins: 65
  Avg Time per Move: 0.16 s
TASK-3 score: 63
         PASSED
```

---

## 🧾 Report Summary

See [`report.tex`](report.pdf) for the detailed report describing:

* Design philosophy and algorithms for each agent
* Heuristics and evaluation functions
* Experimental tuning and trade-offs

---

## 🧑‍💻 Author

**Shivam Chaubey**
B.Tech, Electrical Engineering
Indian Institute of Technology Bombay

* 📧 Email: *[shivamchaubey.iitb@gmail.com](mailto:shivamchaubey.iitb@gmail.com)*
* 🔗 GitHub: [@shivamchaubey100](https://github.com/shivamchaubey100)
* 💼 Interests: AI Agents, Reinforcement Learning, Quantitative Modelling

---

## 🏁 License

This project is released under the **MIT License**.
You are free to use, modify, and distribute it with attribution.

---

### ⭐ Highlights

* Achieved **time-efficient, strong play** under strict runtime limits
* Balanced **search depth and heuristic design**
* Demonstrates practical application of **AI search algorithms**
* Clean, modular code ready for experimentation and extension
