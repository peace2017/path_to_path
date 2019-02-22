from setuptools import setup, find_packages


setup(
    name='path_to_path',
    version='0.0.1',
    author='smironenko',
    company='topcon',
    author_email='smironenko@topcom.com',
    packages=find_packages(),
    entry_points={
        'path_to_path': [
            'path_to_path = path_to_path.__init__:main',
        ],
    },
    install_requires=[
        line.strip() for line in open('requirements.txt')] + [
        'asic_processing'],

    dependency_links=[
        #"git+ssh://git@mos-git.topcon.com:7999/mcrnd/asic_processing.git#egg=asic_processing"]
        "git+ssh://git@mos-git.topcon.com:7999/mc/asic_processing.git#egg=asic_processing"]
)
