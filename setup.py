import re
import setuptools


# Grab the readme
try:
    with open("README.md", "r") as a:
        long_description = a.read()
except Exception:
    long_description = ""


# Steal some code from Novus to get the version
version = ""
with open("voxelbotutils/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)


# Make sure there's a version
if not version:
    raise RuntimeError("version is not set")


# Add a commit reference if we're installing an alpha version
if version.endswith(("a", "b", "rc")):
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += out.decode("utf-8").strip()
        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass


# Set up the requirements
requirements = [
    # Main requirements
    "novus>=0.0.8",
    "toml",
    "aiosqlite",
    "aioredis>=1.3,<2.0",
    "aioredlock>=0.7.0,<0.8",
    "aiodogstatsd>=0.14.0,<0.15",
    "aiohttp",  # no versioning here because I trust u
    "upgradechatpy>=1.0.3,<2.0",
    # Web requirements
    # No versioning on most simply because Pip
    # doesn't like installing very quickly if I keep it
    "cryptography",
    "aiohttp_jinja2",
    "aiohttp_session",
    "jinja2>=3.0.0,<4.0.0",
    "markdown",
    "htmlmin",
]


# Here are some MORE requirements
extras = {
    "docs": [
        "sphinx",
        "sphinx_rtd_theme",
    ],
    "postgres": [
        "asyncpg<0.22",
    ],
    "mysql": [
        "aiomysql",
    ],
}


# And we love setuptools
setuptools.setup(
    name="voxelbotutils",
    version=version,
    author="Kae Bartlett",
    author_email="kae@voxelfox.co.uk",
    description="A set of bot utilities for Novus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Voxel-Fox-Ltd/VoxelBotUtils",
    packages=setuptools.find_packages() + ["discord.ext.vbu"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require=extras,
    entry_points={
        "console_scripts": [
            "voxelbotutils=voxelbotutils.__main__:main",
            "vbu=voxelbotutils.__main__:main",
        ],
    },
    package_data={"voxelbotutils": ["config/*"]},
)
