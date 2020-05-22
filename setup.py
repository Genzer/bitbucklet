from setuptools import setup, find_packages

setup(
    name='bitbucklet',
    description = "A small CLI to manage BitBucket Cloud",
    author = "Genzer Hawker",
    author_email = "genzers@gmail.com",
    version='0.4.0-dev',
    py_modules=['bitbucklet.cli'],
    packages = find_packages(),
    install_requires=[
        'Click',
        'requests',
        'python-dotenv',
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        bitbucklet=bitbucklet.cli:main
    ''',
)