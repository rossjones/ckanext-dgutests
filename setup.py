from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-dgutests',
	version=version,
	description="",
	long_description="""\
	""",
	classifiers=[],
	keywords='',
	author='Ross Jones',
	author_email='ross@servercode.co.uk',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.dgutests'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'selenium==2.28.0',
		'requests==0.14.0'
	],
	entry_points=\
	"""
        [paste.paster_command]
        runtests = ckanext.dgutests.command:TestRunner
	""",
)
