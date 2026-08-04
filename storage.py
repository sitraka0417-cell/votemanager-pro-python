"""Sauvegarde locale (JSON) et export texte des resultats."""
import json
import os
from models import Project

SAVE_DIR = os.path.join(os.path.expanduser("~"), "VoteManagerPro", "saves")


def ensure_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def save_project(project: Project):
    ensure_dir()
    safe_name = "".join(c for c in project.name if c not in '\\/:*?"<>|') or "projet"
    path = os.path.join(SAVE_DIR, f"{safe_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)
    return path


def list_projects():
    ensure_dir()
    names = [f[:-5] for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
    return sorted(names)


def load_project(name):
    path = os.path.join(SAVE_DIR, f"{name}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Project.from_dict(data)


def delete_project(name):
    path = os.path.join(SAVE_DIR, f"{name}.json")
    if os.path.exists(path):
        os.remove(path)


def export_txt(project: Project, filter_mode="all"):
    lines = [f"=== {project.name} ===", ""]
    if not project.sections:
        lines.append("(Aucune section)")
    for s in project.sections:
        ranked = s.ranked()
        total = s.total()
        lines.append(f"-- {s.title or 'Section'} (Top {s.threshold}) --")
        lines.append(f"Total votes : {total}")
        for i, c in enumerate(ranked):
            elected = total > 0 and s.threshold > 0 and i < s.threshold
            if filter_mode == "elected" and not elected:
                continue
            if filter_mode == "non_elected" and elected:
                continue
            pct = round(c.score / total * 100) if total > 0 else 0
            tag = "  [ELU]" if elected else ""
            lines.append(f"  {i + 1}. {c.name or 'Sans nom'} - {c.score} voix ({pct}%){tag}")
        lines.append("")
    return "\n".join(lines)
