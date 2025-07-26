# File operations logic

# ─────── Folder Organization Logic ───────
def create_folders(folder_path, preset, custom_folder=None):
    from logic.constants import EMOJI_MAP
    import os
    try:
        if preset == "📂 Create Default":
            folders = [f"{EMOJI_MAP['Gaming']} Gaming", f"{EMOJI_MAP['School']} School", f"{EMOJI_MAP['Work']} Work", f"{EMOJI_MAP['Projects']} Projects"]
        elif preset != "✨ Custom":
            folders = [f"{EMOJI_MAP.get(preset, '')} {preset}"]
        else:
            folders = [f"{EMOJI_MAP.get('Custom', '')} {custom_folder}"] if custom_folder else []

        for folder in folders:
            dest_folder = os.path.join(folder_path, folder)
            os.makedirs(dest_folder, exist_ok=True)

    except Exception as e:
        raise RuntimeError(f"Failed to create folders - {str(e)}")
