from setuptools import setup

setup(
    name="snapshotalyzer-30000",
    version="0.1",
    author="Chris Pierce",
    author_email="chrisjpierce@gmail.com",
    description="Snapshotalyzer-30000 is a tool to manage EC2 volume snapshots.",
    license="None",
    packages=["shotty"],
    url="https://github.com/indychris70/snapshotalyzer-30000",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli 
    '''
)