from setuptools import setup, find_packages

setup(
    name="py-spam-hunter-client",
    version="1.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'aiohttp',
        'requests',
        'langdetect'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    author="Makar",
    author_email="makar.mikhalchenko@bk.ru",
    description="A client for SpamHunter API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/MakarMS/py-spam-hunter-client",
)
