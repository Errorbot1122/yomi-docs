# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "YOMIH Modding Docs"
copyright = "2026-present, Errorbot1122 and the YOMI Hustle Community (CC BY-SA 4.0)"
author = "Errorbot1122"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.intersphinx"]
intersphinx_mapping = {
    "godot": ("https://docs.godotengine.org/en/3.5/", None),
}

templates_path = ["_templates"]
exclude_patterns = [".*", "**/.*", "_build", "_tools", "_tmp", "_tools"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["godot.css", "custom.css"]
html_js_files = ["custom.js"]
html_theme_options = {
    "collapse_navigation": True,
    "navigation_depth": 10,  # Ensures it reads deep enough into your class structures
}

rst_prolog = """
.. role:: badge-export
.. role:: badge-onready
.. role:: underline
    :class: underline
.. role:: strike
    :class: strike
"""

master_doc = "index"
