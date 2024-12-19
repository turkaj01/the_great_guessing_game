from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Secret key for session management

@app.route("/", methods=["GET", "POST"])
def index():
    # If no random number exists in session, create one
    if 'random_number' not in session:
        session['random_number'] = random.randint(1, 100)
        session['attempts'] = 0  # Track the number of attempts

    feedback = None
    guess = None
    attempts = session['attempts']

    if request.method == "POST":
        try:
            guess = int(request.form['guess'])
            session['attempts'] += 1
            attempts = session['attempts']

            if guess < session['random_number']:
                feedback = "Your guess is too low!"
            elif guess > session['random_number']:
                feedback = "Your guess is too high!"
            else:
                feedback = f"Congratulations! You guessed the correct number in {attempts} attempts!"
                session.clear()  # Clear session to restart the game
                return redirect("/")  # Restart the game after success

            # If the number of attempts is 5, game over
            if attempts >= 5:
                feedback = f"You've used all your attempts. The number was {session['random_number']}. You lose!"
                session.clear()  # Clear session to reset the game
                return redirect("/")  # Restart the game after 5 attempts

        except ValueError:
            feedback = "Please enter a valid number."

    return render_template('index.html', feedback=feedback, attempts=attempts, guess=guess)

if __name__ == "__main__":
    app.run(debug=True)
