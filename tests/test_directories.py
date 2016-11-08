from context import libdesktop

def test_get():

	for i in ['videos', 'documents', 'pictures', 'music', 'downloads', 'desktop']:
		print(i.capitalize() + ':', getattr(libdesktop.directories, 'get_%s_dir' % i)())

	print('-' * 50)
