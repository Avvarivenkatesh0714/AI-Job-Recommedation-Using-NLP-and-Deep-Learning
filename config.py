import os

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

class Config:
    SECRET_KEY = "your_secret_key"
    UPLOAD_FOLDER = UPLOAD_FOLDER
