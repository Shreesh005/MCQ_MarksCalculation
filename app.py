from flask import Flask, request, render_template, redirect, url_for, send_file
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('score.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_input (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            attempted_question INTEGER,
            correct_question INTEGER,
            incorrect_question INTEGER,
            score REAL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student_name = request.form['student_name']
        attempted_question = int(request.form['attempted_question'])
        correct_question = int(request.form['correct_question'])
        incorrect_question = attempted_question - correct_question
        score = 4*correct_question - incorrect_question

        conn = sqlite3.connect('score.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user_input (student_name, attempted_question, correct_question, incorrect_question, score) VALUES (?, ?, ?, ?, ?)',
            (student_name, attempted_question, correct_question, incorrect_question, score)
        )
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

# Endpoint to download the database file
@app.route('/download-db')
def download_db():
    db_path = 'score.db'
    if os.path.exists(db_path):
        return send_file(db_path, as_attachment=True)
    else:
        return "Database file not found.", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
