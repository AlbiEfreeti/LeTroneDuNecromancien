import os
import subprocess
import winshell
from win32com.client import Dispatch

# --- Configuration ---
MAIN_SCRIPT = "main.py"       # Your main python file
ICON_FILE = "necromancer_desktop_icon.ico"     # Must be a real .ico file
EXE_NAME = "LeTroneDuNecromancien"        # The final name you want for your .exe

def build_exe():
    print(f"1. Compiling {MAIN_SCRIPT} into {EXE_NAME}.exe...")
    
    cmd = [
        "py", "-m", "PyInstaller",  # Use PyInstaller as a module
        "--onedir",           # Pack everything into a single .exe
        "--noconsole",         # Hide the black command prompt window
        f"--icon={ICON_FILE}", # Embed icon inside the .exe
        f"--name={EXE_NAME}",  # Output name
        MAIN_SCRIPT
    ]
    
    # Run PyInstaller
    subprocess.run(cmd, check=True)
    print("   Compilation finished successfully.")

def create_desktop_shortcut():
    print("\n2. Creating desktop shortcut...")
    
    # Path to the newly created .exe in the 'dist' folder
    exe_path = os.path.abspath(os.path.join("dist", f"{EXE_NAME}.exe"))
    icon_path = os.path.abspath(ICON_FILE)
    
    # Get the path to the current user's desktop
    desktop_dir = winshell.desktop()
    shortcut_path = os.path.join(desktop_dir, f"{EXE_NAME}.lnk")
    
    # Generate the Windows shortcut (.lnk file)
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.IconLocation = icon_path
    shortcut.save()
    
    print(f"   Success! Shortcut created on your Desktop: {shortcut_path}")

if __name__ == "__main__":
    try:
        build_exe()
        create_desktop_shortcut()
    except Exception as e:
        print(f"\n An error occurred: {e}")
