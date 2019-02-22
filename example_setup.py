from setuptools import setup, find_packages


setup(
    name='alpha_test_tools',
    version='0.0.1',
    author='afomin',
    company='topcon',
    author_email='afomin@topcom.com',
    packages=find_packages(),
    entry_points={
        'sanity_check': [
        'sanity_check = alpha_test_tools.test_plans.sanity_check.sanity_check:main',
        ],
    },
    install_requires=[
        line.strip() for line in open('requirements.txt')] + [
        'asic_processing'],
    dependency_links=[
        "git+ssh://git@mos-git.topcon.com:7999/mcrnd/asic_processing.git#egg=asic_processing"]
)



from setuptools import setup, find_packages
from mc_log_view.utils import version_utils, get_ui

version_utils.update_version_py()

setup(
    name='mc_log_view',
    version='1.1.0',
    author='akalmykov',
    company='topcon',
    author_email='akalmykov@topcom.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mc_log_view = mc_log_view.main:main',
            'data_streamer = tools.data_streamer:main',
            'mclv_crv_converter = tools.mclv_crv_converter:main',
            'crv_mclv_converter = tools.crv_mclv_converter:main',
        ],
    },
    package_data={
        'mc_log_view': get_ui() + [
            'icons/*',
            'field_controller_view/icons/*',
            'vehicle_scene_view/vehicle_scene/items/tank/images/*',
        ]
    },
    install_requires=[
        line.strip() for line in open('requirements.txt')] + [
            'parser-messages',
            'log-player-view',
            'py-gds-client',
            'py-pp-module']
)