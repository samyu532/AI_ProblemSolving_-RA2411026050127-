"""
Cryptarithmetic CSP Solver
--------------------------
Solves puzzles like SEND + MORE = MONEY using Constraint Satisfaction.

Algorithm:
  1. Extract unique letters → variables
  2. Domain: 0–9 for each, except leading letters (domain: 1–9)
  3. Constraints: all-different + arithmetic equality
  4. Backtracking search with forward checking
"""

from itertools import permutations
import re
import time


def parse_puzzle(puzzle: str):
    """
    Parse 'SEND + MORE = MONEY' into words and operator structure.
    Returns (lhs_words, rhs_word, all_letters, leading_letters)
    """
    puzzle = puzzle.strip().upper()
    # Split on '='
    parts = puzzle.split('=')
    if len(parts) != 2:
        raise ValueError("Puzzle must contain exactly one '=' sign.")

    rhs_word = parts[1].strip()
    lhs_parts = parts[0].strip()

    # Extract words from lhs (handles + and -)
    lhs_words = re.findall(r'[A-Z]+', lhs_parts)
    # Detect operators between words
    operators = re.findall(r'[+\-]', lhs_parts)

    if not lhs_words or not rhs_word:
        raise ValueError("Could not parse the puzzle correctly.")

    # Collect all unique letters
    all_letters = list(dict.fromkeys(
        c for word in lhs_words + [rhs_word] for c in word
    ))

    # Leading letters cannot be zero
    leading_letters = set()
    for word in lhs_words + [rhs_word]:
        leading_letters.add(word[0])

    return lhs_words, operators, rhs_word, all_letters, leading_letters
#used for crypt arithmetic problems to solve easily

def word_to_number(word: str, assignment: dict) -> int:
    """Convert a word to its numeric value given a digit assignment."""
    result = 0
    for ch in word:
        result = result * 10 + assignment[ch]
    return result


def check_constraint(lhs_words, operators, rhs_word, assignment):
    """Check if the arithmetic constraint is satisfied."""
    total = word_to_number(lhs_words[0], assignment)
    for i, op in enumerate(operators):
        val = word_to_number(lhs_words[i + 1], assignment)
        if op == '+':
            total += val
        elif op == '-':
            total -= val
    return total == word_to_number(rhs_word, assignment)


def solve_csp(puzzle: str):
    """
    Main CSP solver using backtracking with constraint propagation.
    Returns (solution_dict, time_taken, nodes_explored) or (None, time, nodes).
    """
    lhs_words, operators, rhs_word, all_letters, leading_letters = parse_puzzle(puzzle)

    if len(all_letters) > 10:
        raise ValueError("Too many unique letters (max 10).")

    nodes_explored = [0]
    start = time.time()

    def backtrack(index, assignment, used_digits):
        if index == len(all_letters):
            nodes_explored[0] += 1
            if check_constraint(lhs_words, operators, rhs_word, assignment):
                return dict(assignment)
            return None

        letter = all_letters[index]
        digit_range = range(1, 10) if letter in leading_letters else range(0, 10)

        for digit in digit_range:
            if digit not in used_digits:
                nodes_explored[0] += 1
                assignment[letter] = digit
                used_digits.add(digit)

                result = backtrack(index + 1, assignment, used_digits)
                if result:
                    return result

                del assignment[letter]
                used_digits.remove(digit)

        return None

    solution = backtrack(0, {}, set())
    elapsed = round(time.time() - start, 4)

    return solution, elapsed, nodes_explored[0], lhs_words, operators, rhs_word


def format_solution(solution, lhs_words, operators, rhs_word):
    """Return a human-readable solution string."""
    if not solution:
        return "No solution found."

    lines = []
    lines.append("=== SOLUTION ===")
    lines.append("\nLetter → Digit Mapping:")
    for letter, digit in sorted(solution.items()):
        lines.append(f"  {letter} = {digit}")

    lines.append("\nVerification:")
    nums = [word_to_number(w, solution) for w in lhs_words]
    rhs_num = word_to_number(rhs_word, solution)

    expr_parts = []
    for i, word in enumerate(lhs_words):
        if i > 0:
            expr_parts.append(operators[i-1])
        expr_parts.append(f"{word}({nums[i]})")

    lhs_str = " ".join(expr_parts)
    lines.append(f"  {lhs_str} = {rhs_word}({rhs_num})")

    # Numeric verification
    total = nums[0]
    for i, op in enumerate(operators):
        if op == '+':
            total += nums[i+1]
        else:
            total -= nums[i+1]
    lines.append(f"  Arithmetic check: {total} == {rhs_num} → {'✓ VALID' if total == rhs_num else '✗ INVALID'}")

    return "\n".join(lines)


if __name__ == "__main__":
    puzzle = input("Enter puzzle (e.g., SEND + MORE = MONEY): ").strip()
    solution, elapsed, nodes, lhs_words, operators, rhs_word = solve_csp(puzzle)
    print(format_solution(solution, lhs_words, operators, rhs_word))
    print(f"\nTime: {elapsed}s | Nodes explored: {nodes}")
