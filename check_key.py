"""
check_key.py — run by start.bat to check/collect the Groq API key.
Exits with code 0 if key is present, code 1 on failure.
"""

import os
import sys
from pathlib import Path

ENV_FILE = Path(__file__).parent / ".env"


def read_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def write_key(key: str):
    env = read_env()
    env["GROQ_API_KEY"] = key

    lines = []
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("GROQ_API_KEY"):
                continue          # will re-add below
            lines.append(line)

    # insert GROQ_API_KEY after LMSTUDIO_URL line
    result = []
    inserted = False
    for line in lines:
        result.append(line)
        if "LMSTUDIO_URL" in line and not inserted:
            result.append(f"GROQ_API_KEY={key}")
            inserted = True

    if not inserted:
        result.append(f"GROQ_API_KEY={key}")

    ENV_FILE.write_text("\n".join(result) + "\n", encoding="utf-8")


def main():
    env = read_env()
    key = env.get("GROQ_API_KEY", "").strip()

    if key and key.startswith("gsk_"):
        print("[OK] Groq API key found.")
        return 0

    # Key missing or invalid — show instructions
    import webbrowser

    print()
    print("=" * 62)
    print("          🔑  FREE AI API KEY REQUIRED")
    print("=" * 62)
    print()
    print("  This app uses Groq — a FREE AI service.")
    print("  You only need to do this ONCE.")
    print()
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  HOW TO GET YOUR FREE KEY (takes 2 minutes):        │")
    print("  │                                                     │")
    print("  │  1. Visit  →  https://console.groq.com             │")
    print("  │  2. Click 'Sign Up' and create a free account       │")
    print("  │  3. Click 'API Keys' in the left menu               │")
    print("  │  4. Click 'Create API Key' and give it any name     │")
    print("  │  5. Copy the key  (it starts with: gsk_...)         │")
    print("  │  6. Come back here and paste it below               │")
    print("  └─────────────────────────────────────────────────────┘")
    print()
    print("  Opening console.groq.com in your browser...")
    print()

    try:
        webbrowser.open("https://console.groq.com")
    except Exception:
        pass

    for attempt in range(3):
        try:
            key = input("  Paste your Groq API key here: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            return 1

        if not key:
            print("  [!] Key cannot be empty. Try again.\n")
            continue

        if not key.startswith("gsk_"):
            print('  [!] Key should start with "gsk_". Try again.\n')
            continue

        write_key(key)
        print()
        print("  [OK] API key saved!")
        print()
        return 0

    print("  [ERROR] Too many failed attempts. Please run start.bat again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
