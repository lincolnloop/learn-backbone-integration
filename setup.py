try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='todos',
    version='0.1',
    description='Demo app for demonstrating Backbone.js integration.',
    author='Brandon Konkle',
    author_email='brandon@lincolnloop.com',
    url='http://lincolnloop.com',
    packages=find_packages(),
    scripts=['manage.py'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
