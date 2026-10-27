"""Prepare the existing static assets for Vercel's CDN."""

from pathlib import Path
from shutil import copytree


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    copytree(base_dir / "static", base_dir / "public" / "static", dirs_exist_ok=True)
