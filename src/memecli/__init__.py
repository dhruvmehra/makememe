"""meme - a tiny zero-dependency CLI over the free memegen.link API."""

from .cli import build_url, download, escape, get_templates, get_version, main

__version__ = get_version()
__all__ = ["main", "build_url", "escape", "download", "get_templates", "__version__"]
