import logging
import subprocess
import re
from distutils.core import Command
from setuptools import setup, find_packages


with open("VERSION") as fh:
    __version__ = fh.read().strip()

with open("README.rst", 'r') as readme:
    LONG_DESC = readme.read()

build_version = __version__
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def _run_linters():
    linters = {
        'pylint': ['pylint', '--output-format', 'parseable']
    }

    for linter_name, command in linters.items():
        log.info('Running %s', linter_name)

        if subprocess.call(command + ['bynder_sdk', 'test']):
            raise SystemExit('{} failed'.format(linter_name))


def _run_type_linting():
    if subprocess.call(
            ['mypy',
             '--ignore-missing-imports',
             '--follow-imports=skip',
             'bynder_sdk']):
        raise SystemExit('Type hinting checks failed.')


def _run_tests():
    import pytest
    errno = pytest.main(['--cov-report', 'term-missing:skip-covered',
                         '--cov-report', 'xml',
                         '--cov', 'bynder_sdk',
                         '--cov', 'test',
                         'test'])
    raise SystemExit(errno)


def _run_listdeps():
    regex = re.compile('.*bynder.*')
    bynder_deps = filter(regex.match, requires)
    print(' '.join(bynder_deps))


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        subprocess.call(['pip', 'install'] + test_requires)

    def finalize_options(self):
        pass

    def run(self):
        _run_linters()
        _run_type_linting()
        _run_tests()


class ListDeps(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        _run_listdeps()


class TestDeps(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(' '.join(test_requires))


requires = [
        'requests==2.18.4',
        'requests_oauthlib==0.8.0',
]

test_requires = [
    'pylint==1.7.0',
    'mypy==0.501',
    'pytest',
    'pytest-cov==2.5.1',
]

setup(
    name='bynder-sdk',
    version=build_version,
    description=(
        'Bynder SDK can be used to speed up the'
        ' integration of Bynder in Python'
    ),
    long_description=LONG_DESC,
    url='https://bynder.com',
    author='Bynder',
    author_email='techteam@bynder.com',
    license='MIT',
    cmdclass={'test': PyTest, 'listdeps': ListDeps, 'testdeps': TestDeps},
    packages=find_packages(),
    install_requires=requires,
    tests_require=test_requires,
    include_package_data=True,
    keywords='bynder, dam',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False
)
