"""
Automation tasks, aided by the Invoke package.
"""
import logging
import os
import webbrowser
import sys

from invoke import task
from invoke.runners import Result


DOCS_DIR = 'docs'
DOCS_OUTPUT_DIR = os.path.join(DOCS_DIR, '_build')


@task(default=True, help={
    'all': "Whether to run the tests on all environments (using tox)",
})
def test(ctx, all=False):
    """Run the tests."""
    cmd = 'tox' if all else 'py.test'
    return ctx.run(cmd, pty=True).return_code


@task
def lint(ctx):
    """Run the linter."""
    return ctx.run('flake8 callee tests', pty=True).return_code


@task(help={
    'output': "Documentation output format to produce",
    'rebuild': "Whether to rebuild the documentation from scratch",
    'show': "Whether to show the docs in the browser (default: yes)",
})
def docs(ctx, output='html', rebuild=False, show=True):
    """Build the docs and show them in default web browser."""
    sphinx_build = ctx.run(
        'sphinx-build -b {output} {all} docs docs/_build'.format(
            output=output,
            all='-a -E' if rebuild else ''))
    if not sphinx_build.ok:
        fatal("Failed to build the docs", cause=sphinx_build)

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
    if not yes:
        logging.warning("Aborted -- not uploading to PyPI.")
        return -2

    logging.debug("Uploading version %s to PyPI...", version)
    setup_py_upload = ctx.run('python setup.py sdist upload')
    if not setup_py_upload.ok:
        fatal("Failed to upload version %s to PyPI!", version,
              cause=setup_py_upload)
    logging.info("PyPI upload completed successfully.")

    # add a Git tag and push
    git_tag = ctx.run('git tag %s' % version)
    if not git_tag.ok:
        fatal("Failed to add a Git tag for uploaded version %s", version,
              cause=git_tag)
    git_push = ctx.run('git push && git push --tags')
    if not git_push.ok:
        fatal("Failed to push the release upstream.", cause=git_push)


# Utility functions

def fatal(*args, **kwargs):
    """Log an error message and exit."""
    # determine the exitcode to return to the operating system
    exitcode = None
    if 'exitcode' in kwargs:
        exitcode = kwargs.pop('exitcode')
    if 'cause' in kwargs:
        cause = kwargs.pop('cause')
        if not isinstance(cause, Result):
            raise TypeError(
                "invalid cause of fatal error: expected %r, got %r" % (
                    Result, type(cause)))
        exitcode = exitcode or cause.return_code

    logging.error(*args, **kwargs)
    sys.exit(exitcode or -1)
