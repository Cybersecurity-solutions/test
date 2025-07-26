# ─────── Imports ───────
import os
import sys
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import customtkinter as ctk
import ctypes
import threading
import time
from PIL import Image
import webbrowser

from logic.constants import FILE_TYPES, EMOJI_MAP, DEFAULT_FOLDERS

# from gui.main_window import setup_gui
# from utils.admin import elevate_to_admin

SOCIAL_MEDIA_ASSETS = {
    "discord": "discord.png",
    "github": "github.png",
    "tiktok": "tiktok.png",
    "youtube": "youtube.png"
}

from PIL import Image, ImageDraw

# ─────── Helper Functions ───────
def open_link(url):
    """Safely open a web link in the default browser."""
    try:
        webbrowser.open_new_tab(url)
    except Exception as e:
        print(f"Failed to open link {url}: {e}")
        messagebox.showerror("Error", f"Could not open the link: {url}")
def create_rounded_avatar(image_path, size):
    """Creates a rounded avatar from an image, cropping to a square first."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            
            # Crop the image to a square from the center
            width, height = img.size
            short_dim = min(width, height)
            left = (width - short_dim) / 2
            top = (height - short_dim) / 2
            right = (width + short_dim) / 2
            bottom = (height + short_dim) / 2
            img = img.crop((left, top, right, bottom))

            # Resize to the desired avatar size
            img = img.resize((size, size), Image.Resampling.LANCZOS)

            # Create a circular mask
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)

            # Apply the mask
            img.putalpha(mask)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    except Exception as e:
        print(f"Error creating rounded avatar for {image_path}: {e}")
        return None

def get_category(extension):
    """Determine the category of a file based on its extension."""
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Other"

# ─────── Elevate Script to Administrator ───────
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    python_exe = sys.executable
    script = os.path.abspath(sys.argv[0])
    args = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    params = f'"{script}" {args}'.strip()
    ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, params, None, 1)
    sys.exit()

# ─────── Logging Setup ───────
logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ─────── GUI Setup ───────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x730")
app.title("Folder Organizer Pro")
app.resizable(False, False)

# ✅ Set logo (this must be inside the main block)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # full dir path
    logo_path = os.path.join(script_dir, "Assets", "logo.ico")
    app.iconbitmap(logo_path)
except Exception as e:
    print(f"[!] Failed to load logo: {e}")

# ─────── Tabbed Interface ───────
main_tab = ctk.CTkFrame(app, fg_color="#1e1e1e", corner_radius=12)
settings_tab = ctk.CTkFrame(app, fg_color="#1e1e1e", corner_radius=12)
credits_tab = ctk.CTkFrame(app, fg_color="#1e1e1e", corner_radius=12)

def show_tab(tab_frame):
    """Switch between tabs."""
    for frame in [main_tab, settings_tab, credits_tab]:
        frame.pack_forget()
    tab_frame.pack(fill="both", expand=True)

# ─────── Tab Buttons ───────
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=(15, 10), fill="x")

button_inner_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
button_inner_frame.pack(anchor="center")

for label, frame in [
    ("Main", main_tab),
    ("Settings", settings_tab),
    ("Credits", credits_tab)
]:
    ctk.CTkButton(
        master=button_inner_frame,
        text=label,
        width=120,
        height=35,
        corner_radius=8,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#333333",
        hover_color="#13a100",
        text_color="white",
        command=lambda f=frame: show_tab(f)
    ).pack(side="left", padx=5)

# ─────── Main Tab Content ───────
# Add a header section to the main tab
header_label = ctk.CTkLabel(
    master=main_tab,
    text="Folder Organizer",
    text_color="#ffffff",
    font=ctk.CTkFont(size=20, weight="bold")
)
header_label.pack(pady=(10, 20))

# Group folder selection elements into a frame
folder_selection_frame = ctk.CTkFrame(master=main_tab, fg_color="#2e2e2e", corner_radius=10)
folder_selection_frame.pack(pady=(10, 20), padx=20, fill="x")

status_label = ctk.CTkLabel(
    master=folder_selection_frame,
    text="✅ Ready",
    text_color="#9ca3af",
    font=ctk.CTkFont(size=13, weight="bold")
)
status_label.pack(pady=(5, 10))

def browse_folder():
    """Open a folder selection dialog and start organization."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        log_output.configure(state="normal")
        log_output.insert(tk.END, f"Selected folder: {folder_path}\n")
        log_output.configure(state="disabled")
        # organize_folder_async(folder_path, log_output)  # Removed undefined function

browse_button = ctk.CTkButton(
    master=folder_selection_frame,
    text="📂 Create Folders",
    command=browse_folder,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color="#520000",
    hover_color="#0e7500",
    text_color="white",
    corner_radius=10,
    width=180,  # Adjusted width
    height=50  # Adjusted height
)
browse_button.pack(pady=(5, 10))

def auto_organize_folder():
    """Automatically organize folders alphabetically."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        try:
            folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            folders.sort()  # Sort folders alphabetically

            for folder in folders:
                old_path = os.path.join(folder_path, folder)
                new_path = os.path.join(folder_path, folder)  # Keep folder names unchanged
                os.rename(old_path, new_path)

                log_output.configure(state="normal")
                log_output.insert(tk.END, f"Renamed: {old_path} -> {new_path}\n")
                log_output.configure(state="disabled")

            messagebox.showinfo("Done", "✅ Folders organized alphabetically.")
        except Exception as e:
            error_message = f"Failed to organize folders - {str(e)}"
            logging.error(error_message)
            messagebox.showerror("Error", error_message)

# Move 'AutoOrg' button below 'Browse' button
autoorg_button = ctk.CTkButton(
    master=folder_selection_frame,
    text="📁 Organize Files",
    command=auto_organize_folder,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color="#161616",
    hover_color="#0e7500",
    text_color="white",
    corner_radius=10,
    width=180,  # Adjusted width
    height=50  # Adjusted height
)
autoorg_button.pack(pady=(5, 10))

# Group category selection elements into a frame
category_selection_frame = ctk.CTkFrame(master=main_tab, fg_color="#2e2e2e", corner_radius=10)
category_selection_frame.pack(pady=(10, 20), padx=20, fill="x")

category_label = ctk.CTkLabel(
    master=category_selection_frame,
    text="Select Category:",
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color="#ffffff"
)
category_label.pack(pady=(5, 5))

category_combobox = ttk.Combobox(category_selection_frame, state="readonly", width=30)
category_combobox.pack(pady=(5, 10))
category_combobox['values'] = [
    "📂 Create Default",
    "🎮 Gaming",
    "🎓 School",
    "💼 Work",
    "📂 Projects",
    "✨ Custom"
]
category_combobox.set("📂 Create Default")

custom_folder_label = ctk.CTkLabel(
    master=category_selection_frame,
    text="Custom Folder Name:",
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color="#ffffff"
)
custom_folder_label.pack(pady=(5, 5))

custom_folder_entry = ctk.CTkEntry(
    master=category_selection_frame,
    placeholder_text="Enter folder name",
    font=ctk.CTkFont(size=15, weight="bold")
)
custom_folder_entry.pack(pady=(5, 10))

# Group progress and feedback elements into a frame
progress_feedback_frame = ctk.CTkFrame(master=main_tab, fg_color="#2e2e2e", corner_radius=10)
progress_feedback_frame.pack(pady=(10, 20), padx=20, fill="x")

log_output = scrolledtext.ScrolledText(
    progress_feedback_frame,
    width=70,  # Increase width for more horizontal space
    height=6,  # Restore original height
    font=("Consolas", 12),  # Restore original font size
    bg="#121212",
    fg="#e0e0e0",
    insertbackground="white"
)
log_output.pack(padx=15, pady=(10, 10))
log_output.configure(state="disabled")

# Restore progress bar styling and placement
style = ttk.Style()
style.theme_use("default")
style.configure(
    "TProgressbar",
    troughcolor="#1e1e1e",  # Match the dark theme
    background="#00ff00",  # Green color for progress
    thickness=20  # Increase thickness for better visibility
)

progress_bar = ttk.Progressbar(
    master=progress_feedback_frame,
    orient="horizontal",
    mode="determinate",
    length=400,
    style="TProgressbar"  # Apply the updated style
)
progress_bar.pack(pady=(5, 5))

# Reposition percentage label to be directly underneath the progress bar
percentage_label = ctk.CTkLabel(
    master=progress_feedback_frame,
    text="0%",
    text_color="#ffffff",
    font=ctk.CTkFont(size=12, weight="bold")
)
percentage_label.pack(pady=(5, 5))

# ─────── Folder Organization Logic ───────
from logic.file_operations import create_folders

def run_create_folders(folder_path, preset, custom_folder=None):
    """Create folders using logic.file_operations and update the GUI."""
    try:
        folders = create_folders(folder_path, preset, custom_folder)
        progress_bar['maximum'] = len(folders)

        for i, folder in enumerate(folders, start=1):
            dest_folder = os.path.join(folder_path, folder)
            os.makedirs(dest_folder, exist_ok=True)  # Ensure the folder is created

            progress_bar['value'] = i
            percentage_label.configure(text=f"{round((i / len(folders)) * 100)}%")
            app.update_idletasks()

            log_output.configure(state="normal")
            log_output.insert(tk.END, f"Folder created at: {dest_folder}\n")
            log_output.configure(state="disabled")

        messagebox.showinfo("Done", f"✅ Created {len(folders)} folder(s).")
    except Exception as e:
        error_message = str(e)
        logging.error(error_message)
        messagebox.showerror("Error", error_message)
    finally:
        progress_bar['value'] = 0
        percentage_label.configure(text="0%")

# Replace the call to organize_folder_async with browse_and_create_folders
browse_button.configure(command=lambda: browse_and_create_folders())

def browse_and_create_folders():
    """Browse for folder path and create folders based on user selection."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        preset = category_combobox.get()
        custom_folder = custom_folder_entry.get() if preset == "Custom" else None
        run_create_folders(folder_path, preset, custom_folder)

# ─────── Settings Tab Content ───────
SETTINGS = {
    "use_emojis": True,
    "recursive_scan": True,
    "exclude_hidden": True,
    "min_file_size": 0,
    "duplicate_resolution": "skip",
    "remember_last_config": True
}

settings_label = ctk.CTkLabel(
    master=settings_tab,
    text="Settings",
    text_color="#ffffff",
    font=ctk.CTkFont(size=15, weight="bold")
)
settings_label.pack(pady=(20, 20))

# Add LED toggle back to the settings tab
led_toggle = ctk.CTkSwitch(
    master=settings_tab,
    text="Enable LED Notifications",
    command=lambda: SETTINGS.update({"led_notifications": led_toggle.get(), "led_color": "rainbow"}),
    font=ctk.CTkFont(size=15, weight="bold")
)
led_toggle.pack(pady=(10, 10))

# Define rainbow colors
RAINBOW_COLORS = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#8b00ff"]

# Update LED blinker to apply color only to outer shell frames
def apply_led_shell_only(color):
    try:
        app.configure(bg=color)
        main_tab.configure(fg_color=color)
        settings_tab.configure(fg_color=color)
        credits_tab.configure(fg_color=color)
    except:
        pass

# Update blink_rainbow to use shell-only color application
def blink_rainbow():
    while not stop_event.is_set():
        current_color = RAINBOW_COLORS.pop(0)
        RAINBOW_COLORS.append(current_color)

        app.after(0, lambda c=current_color: apply_led_shell_only(c))

        time.sleep(0.5)

    app.after(0, lambda: apply_led_shell_only(None))  # Let customtkinter theme take over

# Fix LED toggle functionality to properly start and stop rainbow blinking
blinking_thread = None
stop_event = threading.Event()

def start_blinking():
    global blinking_thread, stop_event
    stop_event.clear()
    if blinking_thread and blinking_thread.is_alive():
        return
    blinking_thread = threading.Thread(target=blink_rainbow, daemon=True)
    blinking_thread.start()

def stop_blinking():
    global stop_event
    stop_event.set()
    SETTINGS["led_notifications"] = False
    # Restore default dark theme colors for app and tabs
    app.configure(bg="#1e1e1e")
    main_tab.configure(fg_color="#1e1e1e")
    settings_tab.configure(fg_color="#1e1e1e")
    credits_tab.configure(fg_color="#1e1e1e")

led_toggle.configure(command=lambda: start_blinking() if led_toggle.get() else stop_blinking())

# Add tooltips to UI elements
# Tooltip for Browse button
browse_button.bind("<Enter>", lambda e: status_label.configure(text="Select a folder to organize."))
browse_button.bind("<Leave>", lambda e: status_label.configure(text="✅ Ready"))

# Tooltip for Category dropdown
category_combobox.bind("<Enter>", lambda e: status_label.configure(text="Select a file category to filter files."))
category_combobox.bind("<Leave>", lambda e: status_label.configure(text="✅ Ready"))

# ─────── Credits Tab Content ───────
# Ensure credits_label is properly displayed at the top of the credits_tab
credits_label = ctk.CTkLabel(
    master=credits_tab,
    text="Meet the creators behind Folder Organizer Pro:",
    text_color="#ffffff",
    font=ctk.CTkFont(size=15, weight="bold")
)
credits_label.pack(pady=(20, 10))

# Developer profiles with social links
DEVELOPERS = [
    {
        "name": "Calixto-DEV",
        "title": "Senior Polyglot Software Architect",
        "skills": ["Backend", "Performance", "Clean Code"],
        "socials": {
            "discord": "https://discord.gg/your-server",
            "github": "https://github.com/Calixto-DEV",
            "youtube": "https://youtube.com/your-channel"
        },
        "avatar": "calixto.png"
    },
    {
        "name": "Sergio Maquinna",
        "title": "Junior Software Engineer & UX Designer",
        "skills": ["UX", "Frontend", "Security"],
        "socials": {
            "discord": "https://discord.gg/your-server",
            "tiktok": "https://www.tiktok.com/@sergiomaquinna",
            "youtube": "https://youtube.com/your-channel"
        },
        "avatar": "sergio.png"
    },
    {
        "name": "Davion",
        "title": "Freshman Software Engineer & UX Designer",
        "skills": ["UX", "Frontend", "Security"],
        "socials": {
            "github": "https://github.com/your-profile",
            "discord": "https://discord.gg/your-server",
            "youtube": "https://youtube.com/your-channel"
        },
        "avatar": "test.png"
    }
]


for dev in DEVELOPERS:
    profile_frame = ctk.CTkFrame(master=credits_tab, fg_color="#2e2e2e", corner_radius=10)
    profile_frame.pack(pady=(10, 10), padx=20, fill="x")

    content_frame = ctk.CTkFrame(master=profile_frame, fg_color="transparent")
    content_frame.pack(pady=5, padx=10, fill="x", expand=True)

    # Avatar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    avatar_path = os.path.join(script_dir, "Assets", dev["avatar"])
    avatar_image = create_rounded_avatar(avatar_path, size=64)

    avatar_label = ctk.CTkLabel(master=content_frame, image=avatar_image, text="")
    avatar_label.pack(side="left", padx=(0, 15), pady=5)

    # Details Frame
    details_frame = ctk.CTkFrame(master=content_frame, fg_color="transparent")
    details_frame.pack(side="left", fill="both", expand=True)

    name_label = ctk.CTkLabel(
        master=details_frame,
        text=dev["name"],
        text_color="#ffffff",
        font=ctk.CTkFont(size=14, weight="bold")
    )
    name_label.pack(anchor="w")

    title_label = ctk.CTkLabel(
        master=details_frame,
        text=dev["title"],
        text_color="#9ca3af",
        font=ctk.CTkFont(size=12)
    )
    title_label.pack(anchor="w")

    skills_frame = ctk.CTkFrame(master=details_frame, fg_color="transparent")
    skills_frame.pack(anchor="w", pady=5)

    # Skill tags with different colors
    skill_colors = ["#3b82f6", "#8b5cf6", "#004d0d", "#ef4444", "#f97316", "#eab308", "#84cc16"]
    for i, skill in enumerate(dev["skills"]):
        color = skill_colors[i % len(skill_colors)]
        skill_label = ctk.CTkLabel(
            master=skills_frame,
            text=skill,
            text_color="white",
            fg_color=color,
            corner_radius=5,
            font=ctk.CTkFont(size=10, weight="bold")
        )
        skill_label.pack(side="left", padx=(0, 5))
        # Add padding to the label content
        skill_label.configure(padx=6, pady=2)

    # Social Media Icons
    socials_frame = ctk.CTkFrame(master=details_frame, fg_color="transparent")
    socials_frame.pack(anchor="w", pady=(5, 0))

    for platform, url in dev["socials"].items():
        if platform in SOCIAL_MEDIA_ASSETS:
            try:
                icon_path = os.path.join(script_dir, "Assets", SOCIAL_MEDIA_ASSETS[platform])
                icon_image = Image.open(icon_path).convert("RGBA")
                icon_ctk = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(20, 20))
                
                icon_button = ctk.CTkButton(
                    master=socials_frame,
                    image=icon_ctk,
                    text="",
                    width=10,
                    height=24,
                    fg_color="transparent",
                    hover_color="#444444",
                    command=lambda u=url: open_link(u)
                )
                icon_button.pack(side="left", padx=0)
            except Exception as e:
                print(f"Could not load social icon for {platform}: {e}")

# Add copyright notice
copyright_label = ctk.CTkLabel(
    master=credits_tab,
    text="Cybersecurity-Solution Copyright © 2025",
    text_color="#9ca3af",
    font=ctk.CTkFont(size=12)
)
copyright_label.pack(side="bottom", pady=(20, 10))

# ─────── Finalize GUI ───────
show_tab(main_tab)
app.mainloop()
