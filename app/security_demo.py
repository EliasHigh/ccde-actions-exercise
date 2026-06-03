"""
Beispiel-Datei mit absichtlichen Sicherheitsproblemen fuer die Bandit-Demonstration.
Bandit findet hier 3 typische Sicherheitsluecken – genau wie in der Aufgabe gefordert.
"""
import hashlib
import subprocess

# B105 – Hardcoded Password (Severity: LOW)
# Passwoerter niemals direkt im Code speichern!
password = "supersecret123"


# B324 – Schwacher MD5-Hash (Severity: MEDIUM)
# MD5 gilt als unsicher fuer kryptographische Zwecke (zu leicht zu knacken)
def hash_data(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()


# B602 – subprocess mit shell=True (Severity: HIGH)
# Ermoeglicht Command Injection wenn 'cmd' von aussen kommt
def run_command(cmd: str) -> None:
    subprocess.call(cmd, shell=True)
