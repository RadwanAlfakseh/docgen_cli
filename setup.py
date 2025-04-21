from setuptools import setup, find_packages

setup(
    name='my_cli_app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "pyyaml",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'mycli=my_cli_app.cli:main',
        ],
    },
)
