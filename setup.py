from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="minecraft_manager",
    install_requires=[
        "flask",
        "flask-dotenv",
        "flask-sqlalchemy",
        "flask-session",
        "pyyaml",
        "uwsgi",
        "sentry-sdk[flask]==1.9.8",
        "python-dotenv",
        "flask-inputs",
        "jsonschema",
    ],
    extras_require={},
)
