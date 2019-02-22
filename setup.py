from setuptools import setup, find_packages
from path_to_path.utils import get_ui


setup(
    name='path_to_path',
    version='0.0.1',
    author='smironenko',
    company='topcon',
    author_email='smironenko@topcom.com',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'path_to_path = path_to_path.main:main',
        ],
    },
    install_requires=[
        line.strip() for line in open('requirements.txt')] + [
        'asic_processing'],

    package_data={
        'path_to_path': [
            'main.ui',
            'read_file_dialog/read_file_dialog.ui',
            'read_file_dialog/file_view/file_widget.ui',
            'graph_view/graph_view.ui']
    },

    dependency_links=[
        "git+ssh://git@mos-git.topcon.com:7999/mc/asic_processing.git#egg=asic_processing"]
)
