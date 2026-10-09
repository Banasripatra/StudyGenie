from flask import Flask, render_template, request, jsonify
from datetime import datetime, date, timedelta

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    data = request.json

    name = data.get("name", "Student")
    subjects_text = data.get("subjects", "")
    exam_date_text = data.get("exam_date", "")
    hours = data.get("hours", 3)

    # Subjects
    subjects = [
        s.strip()
        for s in subjects_text.split(",")
        if s.strip()
    ]

    if not subjects:
        return jsonify({
            "error": "Please enter at least one subject."
        }), 400

    # Study hours
    try:
        hours = float(hours)
    except:
        hours = 3

    # Exam date
    try:
        exam_date = datetime.strptime(
            exam_date_text, "%Y-%m-%d"
        ).date()
    except:
        return jsonify({
            "error": "Invalid exam date."
        }), 400

    today = date.today()
    days_remaining = (exam_date - today).days

    if days_remaining < 1:
        days_remaining = 1

    # Create smart personalized plan
    plan_lines = []

    plan_lines.append(
        f"Hello {name}! Here is your personalized StudyGenie plan."
    )
    plan_lines.append("")
    plan_lines.append(
        f"📚 Subjects: {', '.join(subjects)}"
    )
    plan_lines.append(
        f"⏰ Study time: {hours:g} hours/day"
    )
    plan_lines.append(
        f"📅 Days available: {days_remaining}"
    )
    plan_lines.append("")

    for day_number in range(days_remaining):

        current_date = today + timedelta(days=day_number)

        # Decide study stage
        if day_number < days_remaining * 0.6:
            stage = "Concept Building"
        elif day_number < days_remaining * 0.85:
            stage = "Practice & Revision"
        else:
            stage = "Final Revision"

        plan_lines.append(
            f"📅 Day {day_number + 1} — "
            f"{current_date.strftime('%d-%m-%Y')}"
        )
        plan_lines.append(
            f"🎯 Focus: {stage}"
        )

        # Select subjects for the day
        if len(subjects) == 1:
            daily_subjects = subjects
        elif len(subjects) == 2:
            daily_subjects = subjects
        else:
            start = day_number % len(subjects)
            daily_subjects = [
                subjects[start],
                subjects[(start + 1) % len(subjects)]
            ]

        subject_hours = round(
            (hours - 0.5) / len(daily_subjects), 2
        )

        for subject in daily_subjects:

            if stage == "Concept Building":
                task = (
                    f"Study important concepts of {subject} "
                    f"and make short notes."
                )

            elif stage == "Practice & Revision":
                task = (
                    f"Revise {subject}, solve practice questions "
                    f"and identify weak topics."
                )

            else:
                task = (
                    f"Quick revision of {subject}, important formulas, "
                    f"definitions and previous questions."
                )

            plan_lines.append(
                f"   📖 {subject} — {subject_hours:g} hours"
            )
            plan_lines.append(
                f"      → {task}"
            )

        plan_lines.append(
            "   🔄 Revision — 0.5 hour"
        )
        plan_lines.append(
            "      → Revise today's topics and test yourself."
        )
        plan_lines.append("")

    plan_lines.append("💡 StudyGenie Tips:")
    plan_lines.append(
        "• Take a short break after every focused study session."
    )
    plan_lines.append(
        "• Practice questions instead of only reading."
    )
    plan_lines.append(
        "• Revise difficult topics more frequently."
    )
    plan_lines.append(
        "• Keep the last few days mainly for revision."
    )

    smart_plan = "\n".join(plan_lines)

    return jsonify({
        "message": f"Smart Study Plan created for {name}!",
        "exam_date": exam_date.strftime("%d-%m-%Y"),
        "days_remaining": days_remaining,
        "hours_per_day": hours,
        "ai_plan": smart_plan
    })


if __name__ == "__main__":
    app.run(debug=True)