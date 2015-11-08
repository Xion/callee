"""
Automation tasks, aided by the Invoke package.
"""
import os
import webbrowser

from invoke import task, run


DOCS_DIR = 'docs'
DOCS_OUTPUT_DIR = os.path.join(DOCS_DIR, '_build')


@task
def docs(show=True):
    """Build the docs and show them in default web browser."""
    run('sphinx-build docs docs/_build')
    if show:
        webbrowser.open_new_tab(os.path.join(DOCS_OUTPUT_DIR, 'index.html'))
