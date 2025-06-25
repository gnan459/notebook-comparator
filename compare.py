# compare.py
import google.generativeai as genai
import streamlit as st

# ✅ Correct Gemini model name
MODEL_NAME = "gemini-1.5-flash"

# ✅ Load Gemini API key from Streamlit secrets
if "gemini" not in st.secrets or "api_key" not in st.secrets["gemini"]:
    st.error("❌ 'api_key' under [gemini] not found in .streamlit/secrets.toml. Please add it.")
    st.stop()

api_key = st.secrets["gemini"]["api_key"]
genai.configure(api_key=api_key)

# ✅ Initialize model
model = genai.GenerativeModel(model_name=MODEL_NAME)


def compare_cells(cell_a, cell_b):
    prompt = f"""
You are an AI evaluator. Compare the following two Jupyter notebook cells and provide a numeric score representing how different they are.

Score the difference from **0.0 (identical)** to **1.0 (completely different)**.

Respond in **only this format**:
Score: <float between 0.0 and 1.0>

Reference Cell:
{cell_a}

Student Cell:
{cell_b}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # 🛠 Debug (optional): print Gemini output
        # st.write("🔍 Gemini Output:", text)

        lines = text.splitlines()
        score_line = next((l for l in lines if l.lower().startswith("score:")), None)

        if score_line:
            score = float(score_line.split(":")[1].strip())
            return min(max(score, 0.0), 1.0)
        else:
            st.warning("⚠️ No score returned by Gemini.")
            return 0.0

    except Exception as e:
        st.error(f"❌ Gemini error: {e}")
        return 0.0


def evaluate_all_students(reference_nb, student_nb):
    ref_cells = reference_nb.get("cells", [])
    stud_cells = student_nb.get("cells", [])

    total = min(len(ref_cells), len(stud_cells))
    total_score = 0.0

    for i in range(total):
        ref_source = "".join(ref_cells[i].get("source", []))
        stud_source = "".join(stud_cells[i].get("source", []))

        score = compare_cells(ref_source, stud_source)
        total_score += score

    final_score = round((total_score / total) * 100, 2) if total > 0 else 0.0
    return final_score
