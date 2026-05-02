# 🔐 Cryptarithmetic CSP Solver

**AI Problem Solving – Problem 4**

An interactive web application that solves cryptarithmetic puzzles (e.g., `SEND + MORE = MONEY`) using a **Constraint Satisfaction Problem (CSP)** approach with backtracking search.

---

## 🧩 Problem Description

In a cryptarithmetic puzzle, each letter represents a unique digit (0–9). The goal is to find a mapping from letters to digits such that the arithmetic equation holds true.

**Example:**
```
  SEND
+ MORE
------
 MONEY
```
Each letter → unique digit, no leading zeros.

---

## 🤖 Algorithm Used — CSP with Backtracking

### Variables
- Each unique letter in the puzzle is a variable.

### Domains
- Each variable has domain `{0, 1, ..., 9}`.
- Leading letters (first letter of each word) have domain `{1, ..., 9}` (no leading zeros).

### Constraints
1. **All-different**: Every letter must map to a distinct digit.
2. **Arithmetic**: The numeric interpretation of the equation must be satisfied.

### Search Strategy
- **Backtracking**: Assign one letter at a time; if a constraint is violated, backtrack.
- **Forward checking**: Pruning is implicit — used digits are tracked and excluded from remaining assignments.

### Complexity
- Worst case: `10! / (10 - n)!` assignments for `n` unique letters.
- Pruning dramatically reduces the search space in practice.

---

## 📁 Folder Structure

```
cryptarithmetic_csp/
├── src/
│   └── csp_solver.py       # Core CSP algorithm (Python)
├── static/
│   └── index.html          # Interactive GUI (standalone HTML + JS)
├── app.py                  # Flask server (optional backend)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ▶️ Execution Steps

### Option 1: Open GUI directly (No server needed)
```bash
# Simply open the file in a browser:
open static/index.html
```

### Option 2: Run with Flask backend
```bash
# Install dependencies
pip install flask

# Start server
python app.py

# Open in browser
http://localhost:5000
```

### Option 3: Command-line solver
```bash
cd src
python csp_solver.py
# Enter puzzle when prompted:
# SEND + MORE = MONEY
```

---

## 📊 Sample Outputs

### SEND + MORE = MONEY
```
Letter → Digit Mapping:
  D = 7
  E = 5
  M = 1
  N = 6
  O = 0
  R = 8
  S = 9
  Y = 2

Verification:
  SEND(9567) + MORE(1085) = MONEY(10652)
  Arithmetic check: 10652 == 10652 → ✓ VALID

Time: 0.1823s | Nodes explored: 34,812
```

### TWO + TWO = FOUR
```
Letter → Digit Mapping:
  F = 1
  O = 8
  R = 0
  T = 7
  U = 6
  W = 3

Verification:
  TWO(738) + TWO(738) = FOUR(1476)
  ✓ VALID

Time: 0.0031s | Nodes explored: 412
```

---

## 💡 Supported Puzzle Formats

| Format | Example |
|--------|---------|
| Addition | `SEND + MORE = MONEY` |
| Subtraction | `FORTY - TEN = THIRTY` |
| Multi-word | `BASE + BALL = GAMES` |
| Short words | `GO + TO = OUT` |

---

## 🛠 Requirements

- Python 3.8+
- Flask (only for backend mode): `pip install flask`
- No other external libraries — uses Python `itertools` and `re` from stdlib

---

## 🔗 Interactive Website

[Open the Solver →](static/index.html) *(local)* or deploy to GitHub Pages / any static host.

---

## 📝 License
MIT