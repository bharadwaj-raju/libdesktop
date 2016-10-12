# This file is part of libdesktop

from libdesktop import system
import sys
import os

def open_file(default_dir=os.path.expanduser('~'), extensions=None, title='Choose a file'):

	if not extensions:
		extensions = []

	if system.get_name() == 'windows':
		pass

	elif system.get_name() == 'mac':
		pass

	else:
		if system.get_name() in ['gnome', 'unity', 'cinnamon']:
			import gi
			gi.require_version('Gtk', '3.0')

			from gi.repository import Gtk

			class FileChooserWindow(Gtk.Window):

				def __init__(self):

					self.path = None

					Gtk.Window.__init__(self, title="")

					dialog = Gtk.FileChooserDialog(title, None,
						Gtk.FileChooserAction.OPEN,
						(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
						Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

					response = dialog.run()

					if response == Gtk.ResponseType.OK:
						self.path = dialog.get_filename()
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

		elif system.get_name() in ['kde', 'lxqt', 'trinity', 'xfce4']:
			from PyQt5 import Qt

			app = Qt.QApplication(sys.argv)

			widget = Qt.QWidget()

			file_name = Qt.QFileDialog(widget, title, default_dir)

			app.exec_()
