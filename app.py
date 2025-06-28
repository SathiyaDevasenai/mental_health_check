from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

QUESTIONS = [
    {"q": "Do you often feel sad or emotionally low?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you find it hard to focus on daily tasks?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you struggle to find interest in things you used to enjoy?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you feel tired or have low energy most of the day?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you find it difficult to get out of bed or start your day?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Have you been avoiding social situations lately?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you often criticize yourself or feel unworthy?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Have you been eating significantly more or less than usual?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you feel disconnected from people or reality?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]},
    {"q": "Do you feel like you're going through the motions without feeling much?", "a": ["Yes", "No", "Sometimes", "Partly Yes"]}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        user_answers = [request.form.get(f'q{i}') for i in range(len(QUESTIONS))]

        # Count answers
        counts = {"Yes": 0, "No": 0, "Sometimes": 0, "Partly Yes": 0}
        for ans in user_answers:
            if ans in counts:
                counts[ans] += 1

        # Generate pie chart
        labels = list(counts.keys())
        values = list(counts.values())
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.axis("equal")
        chart_path = os.path.join("static", "chart.png")
        plt.savefig(chart_path)
        plt.close()

        yes_count = counts["Yes"]
        if yes_count >= 7:
            message = "You may be emotionally overwhelmed. Consider talking to someone or a professional. You're not alone."
        elif yes_count >= 4:
            message = "Some responses suggest stress. Take time for yourself and seek support when needed."
        else:
            message = "You're emotionally balanced for now. Continue practicing self-care."

        return render_template("result.html", name=name, message=message, answers=user_answers, questions=QUESTIONS, chart="chart.png")

    return render_template("index.html", questions=enumerate(QUESTIONS))

if __name__ == "__main__":
    app.run(debug=True)
