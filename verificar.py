"""Ejecuta cada contrato en un proceso limpio y guarda evidencias reproducibles."""
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
evidencias = root / "docs" / "evidencias"
evidencias.mkdir(parents=True, exist_ok=True)
for version in ("inicial", "refactorizada"):
    result = subprocess.run([sys.executable,"-m","unittest","tests.test_contrato","-v"],cwd=root,
        env={**os.environ,"SGSA_VERSION":version,"PYTHONIOENCODING":"utf-8"},capture_output=True,text=True,encoding="utf-8")
    (evidencias / ("pruebas-"+version+".txt")).write_text(result.stdout+result.stderr,encoding="utf-8")
    print(version + ": " + ("OK" if result.returncode == 0 else "FALLO"))
    if result.returncode: raise SystemExit(result.returncode)
result = subprocess.run([sys.executable,"-m","unittest","tests.test_refactorizada","-v"],cwd=root,
    env={**os.environ,"PYTHONIOENCODING":"utf-8"},capture_output=True,text=True,encoding="utf-8")
(evidencias / "robustez.txt").write_text(result.stdout+result.stderr,encoding="utf-8")
print("robustez: " + ("OK" if result.returncode == 0 else "FALLO"))
raise SystemExit(result.returncode)
