"""
Automation tasks, aided by the Invoke package.
"""
import os
import webbrowser

from invoke import task, run


DOCS_DIR = 'docs'
DOCS_OUTPUT_DIR = os.path.join(DOCS_DIR, '_build')


@task
def docs(output='html', rebuild=False, show=True):
    """Build the docs and show them in default web browser."""
    build_cmd = 'sphinx-build -b {output} {all} docs docs/_build'.format(
        output=output,
        all='-a -E' if rebuild else '')
    run(build_cmd)

    if show:
        webbrowser.open_new_tab(os.path.join(DOCS_OUTPUT_DIR, 'index.html'))
