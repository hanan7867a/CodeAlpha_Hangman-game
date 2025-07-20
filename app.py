from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)


words = [
    {"word": "python", "hint": "A popular programming language"},
    {"word": "coding", "hint": "The process of writing computer programs"},
    {"word": "game", "hint": "An activity for amusement or competition"},
    {"word": "computer", "hint": "An electronic device for processing data"},
    {"word": "algorithm", "hint": "A set of steps to solve a problem"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_game():
    word_data = random.choice(words)
    word = word_data["word"]
    hint = word_data["hint"]
    return jsonify({
        "word": word,
        "hint": hint,
        "word_letters": list(set(word)),
        "guessed_letters": [],
        "wrong_guesses": 0,
        "max_wrong": 6
    })

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.json
    word = data["word"]
    word_letters = set(data["word_letters"])
    guessed_letters = set(data["guessed_letters"])
    wrong_guesses = data["wrong_guesses"]
    guess = data["guess"].lower()

    if guess not in 'abcdefghijklmnopqrstuvwxyz':
        return jsonify({
            "message": "Please enter a valid letter.",
            "guessed_letters": list(guessed_letters),
            "wrong_guesses": wrong_guesses,
            "word_letters": list(word_letters)
        })

    if guess in guessed_letters:
        return jsonify({
            "message": "You already guessed that letter!",
            "guessed_letters": list(guessed_letters),
            "wrong_guesses": wrong_guesses,
            "word_letters": list(word_letters)
        })

    guessed_letters.add(guess)

    if guess in word_letters:
        word_letters.remove(guess)
        message = "Good guess!"
    else:
        wrong_guesses += 1
        message = "Wrong guess!"

    return jsonify({
        "message": message,
        "guessed_letters": list(guessed_letters),
        "wrong_guesses": wrong_guesses,
        "word_letters": list(word_letters)
    })

if __name__ == '__main__':
    app.run(debug=True)