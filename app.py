from flask import Flask, request, render_template, flash, redirect, url_for
from resume_analyzer import extract_text, preprocess_text, calculate_similarity

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

# A sample job description (this can be made dynamic later)
JOB_DESCRIPTION = "Looking for a software engineer skilled in Python, machine learning, and NLP."


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            # Save the uploaded file temporarily
            file_extension = file.filename.split(".")[-1]
            file_path = "uploaded_resume." + file_extension
            file.save(file_path)

            # Process the resume
            resume_text = extract_text(file_path)
            cleaned_resume_text = preprocess_text(resume_text)
            match_score = calculate_similarity(cleaned_resume_text, JOB_DESCRIPTION)

            # Flash the match score so it shows once
            flash(f"Match Score: {match_score}%")
            return redirect(url_for("index"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
