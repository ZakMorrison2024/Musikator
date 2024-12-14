from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load questions and music data
with open('questions.json') as f:
    questions_data = json.load(f)
with open('music.json') as f:
    music_data = json.load(f)

user_data = {}  # To store user answers dynamically

@app.route("/")
def index():
    question_index = 0
    question = questions_data[question_index]['question']
    choices = questions_data[question_index]['choices']
    return render_template("index.html", question=question, question_index=question_index, choices=choices)

@app.route("/question", methods=["POST"])
def question():
    global user_data
    answer = request.form['answer']
    question_index = int(request.form['question_index'])

    # Map answers (e.g., yes -> happy, no -> sad for mood question)
    question_id = questions_data[question_index]['id']
    user_data[question_id] = answer

    question_index += 1
    if question_index < len(questions_data):
        question = questions_data[question_index]['question']
        choices = questions_data[question_index]['choices']
        return render_template("index.html", question=question, question_index=question_index, choices=choices)
    else:
        best_song = get_music_suggestions()  # Get only the best song
        return render_template("index.html", best_song=best_song)


def get_music_suggestions():
    global user_data
    print("User Data:", user_data)  # Debugging: Check user input

    # Start with all music
    music_with_scores = []

    # Loop through each song in the music data
    for song in music_data:
        score = 0  # Initialize the score for the song

        # Loop through each user answer and compare it to the song attributes
        for question_id, user_answer in user_data.items():
            # Check if the song has a matching attribute for the question
            if song.get(question_id) == user_answer:
                score += 1  # Increment score if there's a match

        # Add the song and its score to the list
        music_with_scores.append((song, score))

    # Sort the songs by their score in descending order
    music_with_scores.sort(key=lambda x: x[1], reverse=True)

    # Get the song with the highest score
    if music_with_scores:
        best_song = music_with_scores[0][0]  # The song with the highest score
        print("Best Song:", best_song)  # Debugging: Check the best song
        return best_song
    else:
        return None  # In case no songs match

if __name__ == "__main__":
    app.run(debug=True)