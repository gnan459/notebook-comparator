# app.py
import streamlit as st
import pandas as pd
from drive_utils import (
    get_reference_notebook,
    list_student_notebooks_from_subfolders,
    download_notebook,
)
from compare import evaluate_all_students

st.set_page_config(page_title="Notebook Comparator", page_icon="📘")
st.title("📘 Notebook Comparator with LLM Scoring")

files_folder_id = st.text_input("📁 Enter Google Drive Folder ID for 'Files' (Reference)")
students_folder_id = st.text_input("👥 Enter Google Drive Folder ID for 'Students'")

if st.button("🔍 Start Evaluation") and files_folder_id and students_folder_id:
    with st.spinner("📥 Loading reference notebook..."):
        ref_nb = download_notebook(get_reference_notebook(files_folder_id))

    student_files = list_student_notebooks_from_subfolders(students_folder_id)

    if not student_files:
        st.error("⚠️ No student notebooks found in the provided Drive folder.")
    else:
        results = []
        total = len(student_files)
        progress_bar = st.progress(0)

        for idx, (student_name, file_id) in enumerate(student_files):
            with st.spinner(f"Evaluating {student_name}..."):
                student_nb = download_notebook(file_id)
                score = evaluate_all_students(ref_nb, student_nb)
                results.append({
                    "Student": student_name,
                    "Score": score
                })
                progress_bar.progress((idx + 1) / total)

        df = pd.DataFrame(results)

        st.subheader("📊 Results")
        st.dataframe(df)

        # ✅ Download CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Results as CSV",
            csv,
            "notebook_scores.csv",
            "text/csv"
        )
