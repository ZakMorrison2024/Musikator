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
        suggestions = get_music_suggestions()
        return render_template("index.html", suggestions=suggestions)

def get_music_suggestions():
    global user_data
    print("User Data:", user_data)  # Debugging: Check user input

    # Start with all music
    filtered_music = music_data

    # Filter based on user answers
    for key, value in user_data.items():
        print(f"Filtering for {key} = {value}")  # Debugging: Check filtering criteria
        filtered_music = [m for m in filtered_music if m.get(key) == value]

    print("Filtered Music:", filtered_music)  # Debugging: Check final suggestions
    return filtered_music

if __name__ == "__main__":
    app.run(debug=True)
