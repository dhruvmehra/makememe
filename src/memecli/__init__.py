"""meme - a tiny zero-dependency CLI over the free memegen.link API."""

from .cli import build_url, download, escape, get_templates, main

__version__ = "0.1.1"
__all__ = ["main", "build_url", "escape", "download", "get_templates", "__version__"]
