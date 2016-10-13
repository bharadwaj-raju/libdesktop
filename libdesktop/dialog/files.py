# This file is part of libdesktop

from libdesktop import system
import sys
import os

def open_file(default_dir='~', extensions=None, title='Choose a file', multiple_files=False, directory=False):

	'''Start the native file dialog for opening file(s).

	Starts the system native file dialog in order to open a file (or multiple files).

	The toolkit used for each platform:

	+-------------------------------------+------------------------------+
	| Windows                             | Windows API (Win32)          |
	+-------------------------------------+------------------------------+
	| Mac OS X                            | Cocoa                        |
	+-------------------------------------+------------------------------+
	| GNOME, Unity, Cinnamon, Pantheon    | GTK+ 3                       |
	+-------------------------------------+------------------------------+
	| KDE, LXQt                           | Qt 5 (fallback: Qt 4/GTK+ 3) |
	+-------------------------------------+------------------------------+
	| Other desktops (Xfce, WMs etc)      | GTK+ 2 (fallback: GTK+ 3)    |
	+-------------------------------------+------------------------------+

	**Note on Dependencies**

	It depends on pywin32 for Windows (installed by default in Python for Windows)
	It depends on `PyQt <https://riverbankcomputing.com/software/pyqt>`_ for KDE and LxQt (usually installed by default on these).
	It depends on `PyGObject <https://wiki.gnome.org/Projects/PyGObject>`_ for GNOME etc. (virtually every Linux desktop has this).
	It depends on `PyGTK <https://pygtk.org>`_ for other desktops (not usually installed, so has a GTK+ 3 fallback).

	Args:
		default_dir (str)   : The directory to start the dialog in. Default: User home directory.
		extensions  (dict)  : The extensions to filter by. Format:

							.. code-block:: python

								{
								  'Filter Name (example: Image Files)': ['*.png', '*.whatever', '*']
								}

		title          (str) : The title of the dialog. Default: `Choose a file`
		multiple_files (bool): Whether to choose multiple files or single files only. Default: `False`
		directory      (bool): Whether to choose directories. Default: `False`

	Returns:
		list: `list` of `str` s (each `str` being a selected file). If nothing is selected/dialog is cancelled, it is `None`.
	'''

	default_dir = os.path.expanduser(default_dir)

	if not extensions:
		extensions = {}

	if system.get_name() == 'windows':
		pass  # TODO: Implement Win32 file dialog

	elif system.get_name() == 'mac':
		pass  # TODO: Implement Cocoa file dialog

	else:

		def gtk3_dialog():

			# GTK+ 3

			import gi
			gi.require_version('Gtk', '3.0')

			from gi.repository import Gtk

			class FileChooserWindow(Gtk.Window):

				def __init__(self):

					self.path = ''

					Gtk.Window.__init__(self, title='')

					dialog = Gtk.FileChooserDialog(title, None,
						Gtk.FileChooserAction.OPEN,
						(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
						Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

					if extensions:
						for entry in extensions:
							file_filter = Gtk.FileFilter()
							file_filter.set_name(entry)

							for pattern in extensions[entry]:
								file_filter.add_pattern(pattern)

							dialog.add_filter(file_filter)

					dialog.set_select_multiple(multiple_files)

					dialog.set_current_folder(default_dir)

					response = dialog.run()

					if response == Gtk.ResponseType.OK:
						self.path = dialog.get_filenames()
						dialog.destroy()

					elif response == Gtk.ResponseType.CANCEL:
						self.path = None
						dialog.destroy()

			win = FileChooserWindow()
			win.connect('destroy', Gtk.main_quit)
			win.connect('delete-event', Gtk.main_quit)
			win.show_all()
			win.destroy()
			win.close()

			return win.path


		def qt5_dialog():

			# Qt 5

			try:
				from PyQt5 import Qt

			except ImportError:
				# The API is the same for what this uses
				from PyQt4 import Qt

			class FileChooserWindow(Qt.QWidget):

				def __init__(self):
					super().__init__()

					extensions_string = ''

					if extensions:
						for entry in extensions:
							# entry → Filter name (i.e. 'Image Files' etc)
							# value → Filter expression (i.e. '*.png, *.jpg' etc)
							extensions_string += '%s (%s);;' % (entry, ' '.join(extensions[entry]))

					else:
						extensions_string = 'All Files (*)'

					dialog = Qt.QFileDialog()

					if multiple_files:
						dialog.setFileMode(Qt.QFileDialog.ExistingFiles)

					if directory:
						dialog.setFileMode(Qt.QFileDialog.Directory)

					dialog.setWindowTitle(title)
					dialog.setDirectory(default_dir)

					dialog.setNameFilter(extensions_string)

					if dialog.exec_():
						self.path = dialog.selectedFiles()

					else:
						self.path = None

			app = Qt.QApplication(sys.argv)

			win = FileChooserWindow()
			win.close()

			if win.path:
				return win.path

			else:
				return None

			app.exec_()


		def gtk2_dialog():

			# GTK+ 2

			import pygtk
			pygtk.require('2.0')

			dialog = gtk.FileChooserDialog(title, None,
                        gtk.FILE_CHOOSER_ACTION_OPEN,
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						gtk.STOCK_OPEN, gtk.RESPONSE_OK))

			dialog.set_default_response(gtk.RESPONSE_OK)

			if extensions:
				for entry in extensions:
					file_filter = gtk.FileFilter()
					file_filter.set_name(entry)

					for pattern in extensions[entry]:
						file_filter.add_pattern(pattern)

					dialog.add_filter(file_filter)

			dialog.set_select_multiple(multiple_files)

			response = dialog.run()

			if response == gtk.RESPONSE_OK:
				return dialog.get_filenames()

			elif response == gtk.RESPONSE_CANCEL:
				return None

			dialog.destroy()


		if system.get_name() in ['gnome', 'unity', 'cinnamon', 'pantheon']:
			return gtk3_dialog()

		elif system.get_name() in ['kde', 'lxqt']:
			try:
				return qt5_dialog()

			except ImportError:
				return gtk3_dialog()

		else:
			try:
				return gtk2_dialog()

			except ImportError:
				return gtk3_dialog()


