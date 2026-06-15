# =============================================
# Exam Tutor AI — Constants & Configuration
# =============================================

GRADES = ["Grade 9", "Grade 10", "Grade 11", "Grade 12"]

SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "English",
]

SUBJECT_ICONS = {
    "Mathematics": "📐",
    "Physics": "⚛️",
    "Chemistry": "🧪",
    "Biology": "🧬",
    "Computer Science": "💻",
    "English": "📚",
}

SUBJECT_COLORS = {
    "Mathematics": ("from-blue-500", "to-indigo-600"),
    "Physics": ("from-purple-500", "to-violet-600"),
    "Chemistry": ("from-green-500", "to-emerald-600"),
    "Biology": ("from-teal-500", "to-cyan-600"),
    "Computer Science": ("from-orange-500", "to-amber-600"),
    "English": ("from-rose-500", "to-pink-600"),
}

ACTION_BUTTONS = [
    {
        "type": "explain_simpler",
        "label": "Explain Simpler",
        "emoji": "🧠",
        "description": "Break it down further",
    },
    {
        "type": "another_example",
        "label": "Give Another Example",
        "emoji": "💡",
        "description": "See a new example",
    },
    {
        "type": "generate_mcqs",
        "label": "Generate 5 MCQs",
        "emoji": "📝",
        "description": "Practice with MCQs",
    },
    {
        "type": "short_notes",
        "label": "Generate Short Notes",
        "emoji": "📋",
        "description": "Quick revision notes",
    },
]

VALID_ACTIONS = {btn["type"] for btn in ACTION_BUTTONS}

EXAMPLE_QUESTIONS = [
    {"subject": "Mathematics", "question": "How do I solve quadratic equations?"},
    {"subject": "Physics", "question": "Explain Newton's second law of motion"},
    {"subject": "Chemistry", "question": "What is the difference between ionic and covalent bonds?"},
]