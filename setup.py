#!/usr/bin/env python
import os
import subprocess
import re

from setuptools import setup
from setuptools import find_packages

kwargs = {
    'name' : 'verbena',
    'description' : 'Python library/application for modelling DSC data',
    'url' : 'verbena.readthedocs.io',
    'author' : 'Martin Craig',
    'author_email' : 'martin.craig@eng.ox.ac.uk',
    'license' : '',
}

def git_version():
    # Full version includes the Git commit hash
    full_version = subprocess.check_output('git describe --dirty', shell=True).decode("utf-8").strip(" \n")

    # Python standardized version in form major.minor.patch.dev<build>
    version_regex = re.compile(r"v?(\d+\.\d+\.\d+(-\d+)?).*")
    match = version_regex.match(full_version)
    if match:
        std_version = match.group(1).replace("-", ".dev")
    else:
        raise RuntimeError("Failed to parse version string %s" % full_version)

    return full_version, std_version

def git_timestamp():
    return subprocess.check_output('git log -1 --format=%cd', shell=True).decode("utf-8").strip(" \n")

def set_metadata(module_dir, version_str, timestamp_str):
    vfile = open(os.path.join(module_dir, "verbena", "_version.py"), "w")
    vfile.write("__version__ = '%s'\n" % version_str)
    vfile.write("__timestamp__ = '%s'\n" % timestamp_str)
    vfile.close()

# Read in requirements from the requirements.txt file.
with open('requirements.txt', 'rt') as f:
    requirements = [l.strip() for l in f.readlines()]

rootdir = os.path.abspath(os.path.dirname(__file__))
_, stdv = git_version()
timestamp = git_timestamp()
set_metadata(rootdir, stdv, timestamp)

try:
    from sphinx.setup_command import BuildDoc
    kwargs["cmdclass"] = {
        'doc' : BuildDoc,
    }
    kwargs["command_options"] = {
        'doc': {
            'version': ('setup.py', stdv),
            'release': ('setup.py', stdv),
            'source_dir': ('setup.py', 'doc'),
            'build_dir': ('setup.py', 'doc'),
        }
    }
except:
    pass

setup(
    packages=find_packages(),
    package_data={},
    version=stdv,
    install_requires=requirements,
    entry_points={
        'console_scripts' : [
            "verbena=verbena.main:main",
        ],
    },
    **kwargs
)