# -*- coding: utf-8 -*-
#
# Verbena documentation build configuration file
#
# This file is execfile()d with the current directory set to its
# containing dir.

# -- General configuration ------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax'
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Verbena'
copyright = u'2019, Martin Craig'
author = u'Martin Craig'
build_dir = u"_build"

version = u'0.0.1'
release = u'0.0.1'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'verbena.tex', u'Verbena documentation',
     u'Martin Craig', 'manual'),
]
