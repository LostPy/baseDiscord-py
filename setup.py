from setuptools import setup, find_packages

import baseDiscord


__doc__ = """This package give a base of Discord Bot to develop quickly a Discord Bot with discord.py."""
__license__ = "CC0 1.0 Universal"


setup(
	name='baseDiscord',
	version='1.0.3',
	author='LostPy',
	description="This package give a base of Discord Bot to develop quickly a Discord Bot with discord.py.",
	long_description=__doc__,
	package_dir = {'baseDiscord': './baseDiscord'},
	package_data = {'': ['LICENSE.txt']},
	include_package_data=True,
	url='https://github.com/LostPy/baseDiscord-py',
	classifiers=[
		"Programming Language :: Python",
		"Development Status :: In progress",
		f"License :: {__license__}",
		"Natural Language :: French",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.8+",
		"Topic :: discord.py",
	],
	license=__license__,
	packages = find_packages(),
	install_requires = [
		'discord.py',
		'discord-py-slash-command',
		'colorama'
	]
)