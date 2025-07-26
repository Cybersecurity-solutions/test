# GUI main window logic

# ─────── GUI Setup ───────
def setup_gui():
    import customtkinter as ctk
    app = ctk.CTk()
    app.geometry("700x730")
    app.title("Folder Organizer")
    app.resizable(False, False)
    return app
