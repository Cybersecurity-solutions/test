# ─────── Constants ───────
FILE_TYPES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".cs"]
}

EMOJI_MAP = {
    "Documents": "📄",
    "Images": "📷",
    "Videos": "🎥",
    "Audio": "🎵",
    "Archives": "📦",
    "Code": "💻",
    "Other": "📁",
    # Folders used by the GUI for quick creation
    "Gaming": "🎮",
    "School": "🎓",
    "Work": "💼",
    "Projects": "📂",
    "Custom": "✨"
}

# Default folder presets offered by the application
DEFAULT_FOLDERS = ["Gaming", "School", "Work", "Projects"]
