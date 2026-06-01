# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'PCBA AOI User Manual'
copyright = '2021-2026'
author = ''

release = '2025.2'
version = '2025.2.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinxcontrib.video',
    'sphinx.ext.autosectionlabel',
    'sphinxemoji.sphinxemoji',
    "sphinx_multiversion",
]

html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
html_static_path = ['_static']

# -- Options for HTML output
# Canonical SOURCE language of the .rst files (see PLAN.md Decision 0).
# Per-language builds override this with `-D language=en`.
language = 'zh_CN'

# gettext translation catalogs live next to the source tree.
locale_dirs = ['locale/']
# One .po file per source document (not a single merged catalog) so
# translation drift is attributable to a specific page.
gettext_compact = False

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- Options to Support pdf build in chinese
latex_engine = 'lualatex'
latex_elements = {
    'preamble': '\\usepackage[UTF8]{ctex}\n',
}


html_theme = 'sphinx_rtd_theme'

latex_engine = 'lualatex'
latex_elements = {
    'preamble': '\\usepackage[UTF8]{ctex}\n',
}
epub_show_urls = 'footnote'

templates_path = [
    "_templates",
]

# sphinx-multiversion
# All branches except 'master'
smv_branch_whitelist = r'^(?!chinese).*$'