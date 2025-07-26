# Admin utility logic

# ─────── Elevate Script to Administrator ───────
def elevate_to_admin():
    import ctypes
    import sys
    import os
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        python_exe = sys.executable
        script = os.path.abspath(sys.argv[0])
        args = " ".join(f'"{arg}"' for arg in sys.argv[1:])
        params = f'"{script}" {args}'.strip()
        ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, params, None, 1)
        sys.exit()
