from setuptools import setup

setup(
    name='bitbucklet',
    description = "A small CLI to manage BitBucket Cloud",
    author = "Genzer Hawker",
    author_email = "genzers@gmail.com",
    version='0.1.0',
    py_modules=['bitbucklet.cli'],
    install_requires=[
        'Click',
        'requests',
        'python-dotenv'
    ],
    entry_points='''
        [console_scripts]
        bitbucklet=bitbucklet.cli:main
    ''',
)