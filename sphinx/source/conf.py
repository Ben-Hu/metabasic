import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Metabasic"
copyright = "2020, Ben Hu"
author = "Ben Hu"
release = "0.2.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
]

exclude_patterns = ["_build"]

templates_path = ["_templates"]

html_theme = "alabaster"

html_theme_options = {
    "description": "Dead simple client for interacting with the Metabase dataset API</br></br></br>",
    "extra_nav_links": {"</br>": ""},
    "github_user": "Ben-Hu",
    "github_repo": "metabasic",
    "github_button": False,
    "github_banner": True,
    "fixed_sidebar": True,
    "show_powered_by": False,
    "sidebar_width": "285px",
    "page_width": "1150px",
    "sidebar_link": "#3E4349",
    "sidebar_link_underscore": "#3E4349",
    "sidebar_hr": "#FFFFFFFF",
    "viewcode_target_bg": "#EEE",
    "anchor_hover_bg": "#FFFFFFFF",
    "code_font_family": "Consolas, Courier New, monospace",
    "font_family": "Arial, Helvetica, sans-serif",
}

html_sidebars = {
    "index": ["about.html", "navigation.html", "searchbox.html"],
    "**": ["about.html", "navigation.html", "searchbox.html"],
}

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
