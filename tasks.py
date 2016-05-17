"""
Automation tasks, aided by the Invoke package.
"""
import logging
import os
import webbrowser
import sys

from invoke import task, run


DOCS_DIR = 'docs'
DOCS_OUTPUT_DIR = os.path.join(DOCS_DIR, '_build')


@task(help={'output': "Documentation output format to produce",
            'rebuild': "Whether to rebuild the documentation from scratch",
            'show': "Whether to show the docs in the browser (default: yes)"})
def docs(output='html', rebuild=False, show=True):
    """Build the docs and show them in default web browser."""
    build_cmd = 'sphinx-build -b {output} {all} docs docs/_build'.format(
        output=output,
        all='-a -E' if rebuild else '')
    run(build_cmd)

    if show:
        path = os.path.join(DOCS_OUTPUT_DIR, 'index.html')
        if sys.platform == 'darwin':
            path = 'file://%s' % os.path.abspath(path)
        webbrowser.open_new_tab(path)


@task(help={'yes': "Whether to actually perform the upload. "
                   "By default, a confirmation is necessary."})
def upload(yes=False):
    """Upload the package to PyPI."""
    # check the packages version
    # TODO: add a 'release' to automatically bless a version as release one
    import callee
    if callee.__version__.endswith('-dev'):
        logging.error("Can't upload a development version to PyPI!")
        return -1

    # run the upload if it has been confirmed by the user
    if not yes:
        answer = raw_input("Do you really want to upload to PyPI [y/N]? ")
        yes = answer.lower() == 'y'
    if yes:
        logging.debug("Running PyPI upload...")
        if run('python setup.py sdist upload'):
            logging.info("PyPI upload completed successfully.")
        else:
            logging.error("Failed to upload to PyPI!")
    else:
        logging.warning("Aborted -- not uploading to PyPI.")
