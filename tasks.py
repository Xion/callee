"""
Automation tasks, aided by the Invoke package.
"""
import logging
import os
import webbrowser
import sys

from invoke import task


DOCS_DIR = 'docs'
DOCS_OUTPUT_DIR = os.path.join(DOCS_DIR, '_build')


@task(default=True, help={
    'all': "Whether to run the tests on all environments (using tox)",
})
def test(ctx, all=False):
    """Run the tests."""
    cmd = 'tox' if all else 'py.test'
    ctx.run(cmd, pty=True)


@task
def lint(ctx):
    """Run the linter."""
    ctx.run('flake8 callee tests')


@task(help={
    'output': "Documentation output format to produce",
    'rebuild': "Whether to rebuild the documentation from scratch",
    'show': "Whether to show the docs in the browser (default: yes)",
})
def docs(ctx, output='html', rebuild=False, show=True):
    """Build the docs and show them in default web browser."""
    build_cmd = 'sphinx-build -b {output} {all} docs docs/_build'.format(
        output=output,
        all='-a -E' if rebuild else '')
    ctx.run(build_cmd)

    if show:
        path = os.path.join(DOCS_OUTPUT_DIR, 'index.html')
        if sys.platform == 'darwin':
            path = 'file://%s' % os.path.abspath(path)
        webbrowser.open_new_tab(path)


@task(help={
    'yes': "Whether to actually perform the upload. "
           "By default, a confirmation is necessary.",
})
def upload(ctx, yes=False):
    """Upload the package to PyPI."""
    import callee
    version = callee.__version__

    # check the packages version
    # TODO: add a 'release' to automatically bless a version as release one
    if version.endswith('-dev'):
        fatal("Can't upload a development version (%s) to PyPI!", version)

    # run the upload if it has been confirmed by the user
    if not yes:
        answer = raw_input("Do you really want to upload to PyPI [y/N]? ")
        yes = answer.lower() == 'y'
    if yes:
        logging.debug("Uploading version %s to PyPI...", version)
        if ctx.run('python setup.py sdist upload'):
            logging.info("PyPI upload completed successfully.")
        else:
            fatal("Failed to upload version %s to PyPI!", version)
    else:
        logging.warning("Aborted -- not uploading to PyPI.")
        return -2

    # add a Git tag and push
    if not ctx.run('git tag %s' % version):
        fatal("Failed to add a Git tag for uploaded version %s", version)
    if not ctx.run('git push && git push --tags'):
        fatal("Failed to push the release upstream.")


# Utility functions

def fatal(*args, **kwargs):
    """Log an error message and exit."""
    exitcode = kwargs.pop('exitcode', -1)
    logging.error(*args, **kwargs)
    sys.exit(exitcode)
