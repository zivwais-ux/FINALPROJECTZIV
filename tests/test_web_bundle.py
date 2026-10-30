"""deploy/web, the folder Vercel deploys, must match the source it is built from."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_deploy_folder_is_up_to_date():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_web_bundle.py"), "--check"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


def test_deploy_folder_has_no_agent_code():
    files = {str(p.relative_to(ROOT / "deploy" / "web")) for p in (ROOT / "deploy" / "web").rglob("*.py")}
    assert not any(part in f for f in files for part in ("crews", "tools", "main.py", "rag.py"))
    assert "crewai" not in (ROOT / "deploy" / "web" / "pyproject.toml").read_text()
