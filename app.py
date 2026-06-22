from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "flashcards.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


@app.route('/')
def home():

    index = request.args.get('index', 0, type=int)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flashcards")
    cards = cursor.fetchall()

    conn.close()

    if len(cards) == 0:
        return render_template(
            "index.html",
            card=None
        )

    if index < 0:
        index = 0

    if index >= len(cards):
        index = len(cards) - 1

    return render_template(
        "index.html",
        card=cards[index],
        index=index,
        total=len(cards)
    )


@app.route('/add', methods=['GET', 'POST'])
def add_card():

    if request.method == 'POST':

        question = request.form['question']
        answer = request.form['answer']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO flashcards(question, answer) VALUES (?, ?)",
            (question, answer)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_card(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == 'POST':

        question = request.form['question']
        answer = request.form['answer']

        cursor.execute(
            "UPDATE flashcards SET question=?, answer=? WHERE id=?",
            (question, answer, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    cursor.execute(
        "SELECT * FROM flashcards WHERE id=?",
        (id,)
    )

    card = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        card=card
    )


@app.route('/delete/<int:id>')
def delete_card(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM flashcards WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)