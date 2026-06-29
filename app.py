import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
import google.generativeai as genai
from flask import send_file

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Summarize Route
@app.route("/summarize", methods=["POST"])
def summarize():

    text = request.form.get("text")
    mode = request.form.get("mode")

    if mode == "technical":
        instruction = """
        Use technical terminology.
        Preserve important concepts.
        Generate exactly 3 bullet points.
        """
    elif mode == "detailed":
        instruction = """
        Generate informative summaries.
        Exactly 3 bullets.
        Each bullet can contain two sentences.
        """
    elif mode == "executive":
        instruction = """
        Write the summary for a manager.
        Focus on key decisions and outcomes.
        Exactly 3 bullets.
        """
    else:
        instruction = """
        Write concise summaries.
        Exactly 3 bullets.
        Simple English.
        """

    if not text or text.strip() == "":
        return render_template(
            "index.html",
            error="Please enter some text."
        )

    prompt = f"""
    You are an expert AI summarizer.
    {instruction}
    Text:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        summary = response.text

        return render_template(
            "index.html",
            summary=summary,
            original=text,
            mode=mode
        )

    except Exception:
        return render_template(
            "index.html",
            error="Unable to generate summary. Please check your internet connection or API key."
        )

@app.route("/download", methods=["POST"])
def download():
    summary = request.form.get("summary")
    filename = "exports/summary.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("# AI Summary\n\n")
        file.write(summary)

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
  