import os
import shutil
import tempfile
from pathlib import Path

def clear_folder(folder):
    if not os.path.exists(folder):
        return

    print(f"\nCleaning: {folder}")

    for item in os.listdir(folder):
        path = os.path.join(folder, item)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)

        except Exception as e:
            print(f"Skipped: {path} ({e})")

folders = [
    tempfile.gettempdir(),                     # User Temp
    r"C:\Windows\Temp",                        # Windows Temp
    r"C:\Windows\Prefetch",                    # Prefetch
    r"C:\Windows\SoftwareDistribution\Download" # Windows Update Cache
]

for folder in folders:
    clear_folder(folder)

print("\nEmptying Recycle Bin...")

try:
    os.system('powershell -Command "Clear-RecycleBin -Force"')
except:
    pass

print("\nCleanup completed.")

input("\nPress Enter to exit...")