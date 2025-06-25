import nbformat
import io
import os
import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

# ✅ Load Google service account credentials

creds = service_account.Credentials.from_service_account_info(
        st.secrets["google"]
    )


# ✅ Build Drive API client
service = build("drive", "v3", credentials=creds)


def get_reference_notebook(files_folder_id):
    """Get the first .ipynb file from the reference 'Files' folder."""
    results = service.files().list(
        q=f"'{files_folder_id}' in parents and name contains '.ipynb'",
        fields="files(id, name)",
        orderBy="modifiedTime desc",
        supportsAllDrives=True,
    ).execute()

    files = results.get("files", [])
    if not files:
        raise Exception("❌ No .ipynb file found in Files folder.")
    
    # Debug log
    print("✅ Reference notebook found:", files[0]["name"])
    return files[0]["id"]


def list_student_notebooks_from_subfolders(students_folder_id):
    """List the latest .ipynb notebook from each student's subfolder."""
    student_notebooks = []

    # List student subfolders
    subfolders = service.files().list(
        q=f"'{students_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)",
        supportsAllDrives=True,
    ).execute().get("files", [])

    for folder in subfolders:
        folder_id = folder["id"]
        folder_name = folder["name"]

        # Get the latest .ipynb file in each subfolder
        files = service.files().list(
            q=f"'{folder_id}' in parents and name contains '.ipynb'",
            fields="files(id, name, modifiedTime)",
            orderBy="modifiedTime desc",
            supportsAllDrives=True,
        ).execute().get("files", [])

        if files:
            student_notebooks.append((folder_name, files[0]["id"]))

    return student_notebooks


def download_notebook(file_id):
    """Download a .ipynb file and return it as a parsed nbformat notebook."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    return nbformat.read(fh, as_version=4)
