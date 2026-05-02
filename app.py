"""
Flask API server for the Cryptarithmetic CSP Solver GUI.
Run: python app.py
"""

from flask import Flask, request, jsonify, send_from_directory
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from csp_solver import solve_csp, format_solution, word_to_number

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    puzzle = data.get('puzzle', '').strip()

    if not puzzle:
        return jsonify({'error': 'No puzzle provided.'}), 400

    try:
        solution, elapsed, nodes, lhs_words, operators, rhs_word = solve_csp(puzzle)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

    if not solution:
        return jsonify({
            'solved': False,
            'message': 'No solution exists for this puzzle.',
            'time': elapsed,
            'nodes': nodes
        })

    # Build word values
    word_values = {}
    for w in lhs_words + [rhs_word]:
        word_values[w] = word_to_number(w, solution)

    lhs_nums = [word_to_number(w, solution) for w in lhs_words]
    rhs_num = word_to_number(rhs_word, solution)

    return jsonify({
        'solved': True,
        'mapping': solution,
        'words': {
            'lhs': lhs_words,
            'operators': operators,
            'rhs': rhs_word
        },
        'values': word_values,
        'lhs_nums': lhs_nums,
        'rhs_num': rhs_num,
        'time': elapsed,
        'nodes': nodes
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)