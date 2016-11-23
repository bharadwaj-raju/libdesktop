# coding: utf-8

# This file is part of libdesktop

# The MIT License (MIT)
#
# Copyright (c) 2016 Bharadwaj Raju
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
from libdesktop import system

__WINDOWS_FOLDER_GUIDS = {
	'Desktop': '{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}',
	'Documents': '{FDD39AD0-238F-46AF-ADB4-6C85480369C7}',
	'Downloads': '{374DE290-123F-4565-9164-39C4925E467B}',
	'Music': '{4BD8D571-6D19-48D3-BE97-422220080E43}',
	'Pictures': '{33E28130-4E1E-4676-835A-98395C3BC3BB}',
	'Videos': '{18989B1D-99B5-455B-841C-AB7C74E4DDFC}',
	'Public': '{DFDF76A2-C82A-4D63-906A-5644AC457385}',
	'ProgramFiles': '{905e63b6-c1bf-494e-b29c-65b732d3d21a}',
	'ProgramFilesx64': '{6D809377-6AF0-444b-8957-A3773F02200E}',
	'ProgramFilesx86': '{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}',
	'Windows': '{F38BF404-1D43-42F2-9305-67DE0B28FC23}',
	'System32': '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}'
}


def __unix_get_user_dirs():

	with open(os.path.join(get_config_file('user-dirs.dirs')[0])) as f:
		user_dirs = {}
		for line in f:
			if not line.startswith('#') and '=' in line:
				user_dirs[
					line.split(
						'=',
						1)[0]] = os.path.expanduser(
					line.split('=')[1].replace(
						'"',
						'').replace(
						"'",
						'').replace(
						'$HOME',
						'~').strip())

	return user_dirs


def __unix_get_dir(unix_dir):

	return os.path.expanduser(__unix_get_user_dirs().get(
		'XDG_%s_DIR' % unix_dir.upper(), '~/%s' % unix_dir))


def __windows_get_dir(win_dir):

	from win32com.shell import shell

	df = shell.SHGetDesktopFolder()
	pidl = df.ParseDisplayName(0, None,
							   '::%s' % __WINDOWS_FOLDER_GUIDS[win_dir])[1]

	return shell.SHGetPathFromIDList(pidl)


def __mac_get_dir(mac_dir):

	from Carbon import Folder, Folders

	dir_var = getattr(Folders, 'k%sFolderType' % mac_dir)

	folderref = Folder.FSFindFolder(Folders.kUserDomain,
									dir_var, False)

	return folderref.as_pathname()


def __get_dir(user_dir):
	if system.get_name() == 'windows':
		return __windows_get_dir(user_dir)

	elif system.get_name() == 'mac':
		return __mac_get_dir(user_dir)

	else:
		return __unix_get_dir(user_dir)


def get_videos_dir():
	'''Get the user directory for videos.

	Get the user directory for storing videos.

	Returns:
			str: The path to the user Videos directory.
	'''

	return __get_dir('Videos')


def get_pictures_dir():
	'''Get the user directory for pictures.

	Get the user directory for storing pictures.

	Returns:
			str: The path to the user Pictures directory.
	'''

	return __get_dir('Pictures')


def get_documents_dir():
	'''Get the user directory for documents.

	Get the user directory for storing documents.

	Returns:
			str: The path to the user Documents directory.
	'''

	return __get_dir('Documents')


def get_downloads_dir():
	'''Get the user directory for downloads.

	Get the user directory for storing downloaded files.

	Returns:
			str: The path to the user Downloads directory.
	'''

	return __get_dir('Downloads')


def get_desktop_dir():
	'''Get the user desktop directory.

	Get the user directory for storing files on the Desktop.

	Returns:
			str: The path to the user Desktop directory.
	'''

	return __get_dir('Desktop')


def get_music_dir():
	'''Get the user directory for music.

	Get the user directory for storing music.

	Returns:
			str: The path to the user Music directory.
	'''

	return __get_dir('Music')


def get_config_dir(program='', system_wide=False):
	'''Get the configuration directory.

	Get the configuration directories, optionally for a specific program.

	Args:
			program	(str) : The name of the program whose configuration directories have to be found.
			system_wide (bool): Gets the system-wide configuration directories.

	Returns:
			list: A list of all matching configuration directories found.
	'''

	config_homes = []

	if system_wide:
		if os.name == 'nt':
			config_homes.append(
				winreg.ExpandEnvironmentStrings('%PROGRAMDATA%'))

		else:
			config_homes.append('/etc')
			config_homes.append('/etc/xdg')

			if os.name == 'darwin':
				config_homes.append('/Library')

	else:
		if os.name == 'nt':
			import winreg
			config_homes.append(
				winreg.ExpandEnvironmentStrings('%LOCALAPPDATA%'))
			config_homes.append(
				os.path.join(
					winreg.ExpandEnvironmentStrings('%APPDATA%'),
					'Roaming'))
		else:
			if os.getenv('XDG_CONFIG_HOME'):
				config_homes.append(os.getenv('XDG_CONFIG_HOME'))
			else:
				try:
					from xdg import BaseDirectory
					config_homes.append(BaseDirectory.xdg_config_home)
				except ImportError:
					config_homes.append(os.path.expanduser('~/.config'))

				config_homes.append(os.path.expanduser('~'))

				if os.name == 'darwin':
					config_homes.append(os.path.expanduser('~/Library'))

	if program:
		def __find_homes(app, dirs):

			homes = []

			for home in dirs:
				if os.path.isdir(os.path.join(home, app)):
					homes.append(os.path.join(home, app))

				if os.path.isdir(os.path.join(home, '.' + app)):
					homes.append(os.path.join(home, '.' + app))

				if os.path.isdir(os.path.join(home, app + '.d')):
					homes.append(os.path.join(home, app + '.d'))

			return homes

		app_homes = __find_homes(program, config_homes)

		# Special Cases

		if program == 'vim':
			app_homes.extend(__find_homes('vimfiles', config_homes))

		elif program == 'chrome':
			app_homes.extend(__find_homes('google-chrome', config_homes))

		elif program in ['firefox', 'thunderbird']:
			app_homes.extend(
				__find_homes(
					program, [
						os.path.expanduser('~/.mozilla')]))

		return app_homes

	return config_homes


def get_config_file(program, system_wide=False):
	'''Get the configuration file for a program.

	Gets the configuration file for a given program, assuming it stores it in
	a standard location. See also :func:`get_config_dir()`.

	Args:
			program	 (str): The program for which to get the configuration file.
			system_wide (bool):Whether to get the system-wide file for the program.

	Returns:
			list: A list of all matching configuration files found.
	'''

	program_config_homes = get_config_dir(program, system_wide)
	config_homes = get_config_dir(system_wide=system_wide)
	config_files = []

	for home in config_homes:
		for sub in os.listdir(home):
			if os.path.isfile(os.path.join(home, sub)):
				if sub.startswith(program):
					config_files.append(os.path.join(home, sub))

	if not program.startswith('.'):
		config_files.extend(get_config_file('.' + program, system_wide))

	for home in program_config_homes:
		for sub in os.listdir(home):
			if os.path.isfile(os.path.join(home, sub)
							  ) and sub.startswith(program):
				config_files.append(os.path.join(home, sub))

	return config_files


def windows_get_program_files_dir():
	'''Get the Windows system Program Files directory.

	Get the Windows system Program Files directory.

	Returns:
			str: The path to the Windows system Program Files directory.
	'''

	return __windows_get_dir('ProgramFiles')


def windows_get_program_files_x86_dir():
	'''Get the Windows system Program Files (x86) directory.

	Get the Windows system directory for storing 32-bit programs on a 64-bit system, that is, Program Files (x86).

	Note:
			This will return the normal Program Files directory (as given in :func:`windows_get_program_files_dir()`) on a 32-bit system, or a 32-bit Python.

	Returns:
			str: The path to the Windows system Program Files (x86) directory.
	'''

	return __windows_get_dir('ProgramFilesx86')


def windows_get_program_files_x64_dir():
	'''Get the Windows system Program Files (x64) directory.

	Get the Windows system directory for storing 64-bit programs, that is, Program Files (x64).

	Note:
			This will fail (possibly with an interpreter crash) on 32-bit systems, or a 32-bit Python.

	Returns:
			str: The path to the Windows system Program Files (x64) directory.
	'''

	return __windows_get_dir('ProgramFilesx64')


def windows_get_public_dir():
	'''Get the Windows system Public directory.

	Get the Windows system Public directory.

	Returns:
			str: The path to the system Public directory.
	'''

	return __windows_get_dir('Public')


def windows_get_windows_dir():
	'''Get the Windows system directory.

	Get the Windows system Windows directory (example: C:/Windows/)

	Returns:
			str: The path to the Windows system Windows directory.
	'''

	return __windows_get_dir('Windows')


def windows_get_system32_dir():
	'''Get the Windows system System32 directory.

	Get the Windows system System32 directory (example: C:/Windows/System32/)

	Returns:
			str: The path to the Windows system System32 directory.
	'''

	return __windows_get_dir('System32')
