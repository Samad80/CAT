# =============================================
# Exam Tutor AI — Prompt Builders
# =============================================


def build_main_prompt(grade: str, subject: str, question: str) -> str:
    return f"""You are an expert {subject} teacher for high school students.

**Student Grade:** {grade}
**Subject:** {subject}
**Question:** {question}

Please answer this question following these instructions exactly:

1. Answer at the appropriate level for {grade} students — not too simple, not too advanced
2. Use clear, friendly language a student can easily understand
3. Explain step-by-step with numbered steps where appropriate
4. Include relevant formulas or equations if applicable
5. Provide a real-world example to make the concept relatable
6. Mention 2-3 common mistakes students make in exams related to this topic
7. Format your response using the EXACT structure below — use these exact markdown headers:

## 📖 Explanation

[Main explanation here - step by step]

## 🔑 Key Concepts

[Bullet list of key concepts and definitions]

## 📐 Formulas & Equations

[List relevant formulas. If no formulas apply, write "No specific formulas needed for this concept."]

## 🌍 Real-World Example

[A concrete, relatable real-world example]

## 🎯 Exam Tips

[2-3 specific tips for answering this type of question in an exam]

## ⚠️ Common Mistakes

[2-3 common mistakes students make — be specific]

Keep the tone encouraging and academic. Focus on concepts commonly tested in {grade} exams."""


def build_action_prompt(action: str, grade: str, subject: str, previous_answer: str) -> str:
    context = f"Grade: {grade} | Subject: {subject}"

    prompts = {
        "explain_simpler": f"""You previously explained a {subject} concept to a {grade} student. Here was your explanation:

{previous_answer}

Now explain the same concept in an EVEN SIMPLER way. Use:
- Very simple, everyday language
- Short sentences
- Simple analogies (compare to things from daily life)
- Smaller, more digestible steps
- Avoid jargon completely

Context: {context}

Format your response with clear sections using markdown headers. Make it feel like you're talking to a friend.""",

        "another_example": f"""You explained a {subject} concept to a {grade} student. Here was your explanation:

{previous_answer}

Now provide a COMPLETELY DIFFERENT real-world example that illustrates the same concept. The example should:
- Be from a different domain or context than the previous example
- Be relatable to a {grade} student's daily life
- Clearly show how the concept applies
- Include any relevant numbers or calculations

Context: {context}

Use markdown formatting with clear sections.""",

        "generate_mcqs": f"""Based on this {subject} explanation for {grade} students:

{previous_answer}

Generate exactly 5 multiple-choice questions (MCQs) that test understanding of this concept.

Format EXACTLY like this:

## 📝 Practice MCQs

**Question 1:** [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

✅ **Answer:** [Correct option letter] — [Brief explanation of why]

---

**Question 2:** [Question text]
...and so on for all 5 questions.

Make questions range from easy (Q1-Q2) to medium (Q3-Q4) to harder (Q5). Focus on concepts that appear in {grade} exams.""",

        "short_notes": f"""Based on this {subject} explanation for {grade} students:

{previous_answer}

Create concise short notes / revision summary. Format EXACTLY like this:

## 📋 Quick Revision Notes

### Topic: [Topic Name]
**Grade:** {grade} | **Subject:** {subject}

---

### ⚡ Core Concept
[1-2 sentence summary of the main idea]

### 🔑 Key Points
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4]
- [Point 5]

### 📐 Must-Know Formulas
[List formulas or "N/A" if not applicable]

### 🧠 Memory Tricks
[1-2 mnemonics or memory aids]

### ⚠️ Don't Forget
[2-3 most important things to remember for the exam]

Keep it concise — this is for last-minute revision before an exam.""",
    }

    return prompts.get(action, build_main_prompt(grade, subject, previous_answer))