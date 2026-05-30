import os
import subprocess
import time
from pathlib import Path

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=False)

print("=" * 40)
print("Mounting EFI partition...")
print("=" * 40)

run("mountvol S: /s")

policy_dir = Path(r"S:\EFI\Microsoft\Boot\CiPolicies\Active")

print("\n" + "=" * 40)
print("Removing active CI policy files...")
print("=" * 40)

if policy_dir.exists():
    for cip_file in policy_dir.glob("*.cip"):
        try:
            cip_file.unlink()
            print(f"Deleted: {cip_file}")
        except Exception as e:
            print(f"Failed to delete {cip_file}: {e}")
else:
    print("Policy directory not found.")

print("\n" + "=" * 40)
print("Remaining files:")
print("=" * 40)

if policy_dir.exists():
    files = list(policy_dir.iterdir())
    if files:
        for f in files:
            print(f.name)
    else:
        print("(No files found)")
else:
    print("Directory not found.")

print("\n" + "=" * 40)
print("Unmounting EFI partition...")
print("=" * 40)

run("mountvol S: /d")

print("\n" + "=" * 40)
print("DONE")
print("=" * 40)

print("\nRebooting in 10 seconds...")
time.sleep(10)

run("shutdown /r /t 0")
