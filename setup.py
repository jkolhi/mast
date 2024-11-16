from setuptools import setup, find_packages

setup(
    name="mast",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'numpy>=1.19.0',
        'librosa>=0.8.0',
        'matchering>=2.0.0',
        'matplotlib>=3.3.0',
        'mutagen>=1.45.0',
    ],
    entry_points={
        'console_scripts': [
            'mast=main:main',
        ],
    },
    author="JK",
    description="Master Audio Similarity Tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="audio, mastering, similarity, analysis",
    python_requires='>=3.8',
)