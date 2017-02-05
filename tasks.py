"""
Automation tasks, aided by the Invoke package.
"""
import logging
import os
import webbrowser
import sys

from invoke import task
from invoke.exceptions import Exit
from invoke.runners import Result

try:
    input = raw_input
except NameError:
    pass  # Python 3, input() already works like raw_input() in 2.x.


DOCS_DIR = 'docs'
DOCS_OUTPUT_DIR = os.path.join(DOCS_DIR, '_build')


@task(default=True, help={
    'all': "Whether to run the tests on all environments (using tox)",
    'verbose': "Whether to enable verbose output",
})
def test(ctx, all=False, verbose=False):
    """Run the tests."""
    cmd = 'tox' if all else 'py.test'
    if verbose:
        cmd += ' -v'
    return ctx.run(cmd, pty=True).return_code


@task
def lint(ctx):
    """Run the linter."""
    return ctx.run('flake8 callee tests', pty=True).return_code


@task(help={
    'output': "Documentation output format to produce",
    'rebuild': "Whether to rebuild the documentation from scratch",
    'show': "Whether to show the docs in the browser (default: yes)",
    'verbose': "Whether to enable verbose output",
})
def docs(ctx, output='html', rebuild=False, show=True, verbose=True):
    """Build the docs and show them in default web browser."""
    sphinx_build = ctx.run(
        'sphinx-build -b {output} {all} {verbose} docs docs/_build'.format(
            output=output,
            all='-a -E' if rebuild else '',
            verbose='-v' if verbose else ''))
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
        answer = input("Do you really want to upload to PyPI [y/N]? ")
        yes = answer.strip().lower() == 'y'
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
    """Log an error message and exit.

    Following arguments are keyword-only.

    :param exitcode: Optional exit code to use
    :param cause: Optional Invoke's Result object, i.e.
                  result of a subprocess invocation
    """
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
    raise Exit(exitcode or -1)
