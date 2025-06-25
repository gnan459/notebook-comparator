
# 📘 Notebook Comparator with LLM Scoring

This project evaluates student Jupyter notebooks by comparing them with a reference notebook using Google's **Gemini 1.5 Flash** Large Language Model (LLM). It's built with **Streamlit** and integrates with **Google Drive API** for file management.

---

## 🚀 Features

- 🔍 Compares each student's `.ipynb` file to a reference notebook.
- 🤖 Uses Gemini LLM to compute a similarity score (0–100).
- 📊 Displays results in a table.
- 📁 Allows CSV download of evaluation results.
- ☁️ Google Drive integration (reference and student submissions).

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini API (generativeai)**
- **Google Drive API (with Service Account)**
- **nbformat**

---

## 📂 Project Structure

```
notebook-comparator/
├── app.py                  # Main Streamlit app
├── compare.py              # Handles LLM-based notebook comparison
├── drive_utils.py          # Google Drive interaction functions
├── test_gemini.py          # (Optional) Debug Gemini API separately
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignores virtual environment and secrets
├── .gitattributes          # Git line-ending normalization
└── .streamlit/
    └── secrets.toml        # 🔐 Your API keys (NOT included in GitHub)
```

---

## 🔐 Setup Secrets

In `.streamlit/secrets.toml` (do **not** push this to GitHub):

```toml
[google]
type = "service_account"
project_id = "your_project_id"
private_key_id = "your_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
token_uri = "https://oauth2.googleapis.com/token"

[gemini]
api_key = "your_gemini_api_key"
```

---

## ⚙️ Installation & Run

```bash
# Clone the repo
git clone https://github.com/gnan459/notebook-comparator.git
cd notebook-comparator

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---

## 📌 Notes

- Ensure that the **reference notebook** is placed in a Google Drive folder named `Files`.
- Each **student's submission** should be inside a subfolder under a common `Students` folder.
- All files must be in `.ipynb` format.

---

## 📧 Contact

For questions or suggestions, feel free to open an issue or contact [gnan459](https://github.com/gnan459).

---

## 📄 License

This project is licensed under the MIT License.
