# Browse Directory v1.1, 2013-10-13
# by Fredrik Averpil, fredrik.averpil [at] gmail.com, http://fredrikaverpil.tumblr.com
# 
#
# Usage:
# a) select any Write node or Read node and run browseDirByNode()
# b) open any path via command browseDir(path)
# 
# Example of menu.py:
# import browseDir
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Node\'s file path', "browseDir.browseDirByNode()", 'shift+b' )
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder', "browseDir.browseDir('scripts')" )
#
# And if your folder structure looks like this -
# serverpath/ ... sequence_folder/shot_folder/nuke/scripts/
# you should be able to use the following as well:
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder', "browseDir.browseDir('sequence')" )
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder', "browseDir.browseDir('shot')" )
#
#



import nuke
import sys
import os
import subprocess

def launch(directory):
	# Open folder
	print('Attempting to open folder: ' + directory)
	if os.path.exists( directory ):
	        if sys.platform == 'darwin':
	            subprocess.check_call(['open', '--', directory])
	        elif sys.platform == 'linux2':
	            subprocess.check_call(['gnome-open', '--', directory])
	        elif sys.platform == 'win32':
	            os.startfile(directory)
	else:
		nuke.message('Path does not exist:\n' + directory)


def browseDirByNode():

	error = False

	try:
		selectedNodeFilePath = nuke.callbacks.filenameFilter( nuke.selectedNode()['file'].getValue() )

	except ValueError:
		error = True
		nuke.message('No node selected.')
	except NameError:
		error = True
		nuke.message('You must select a Read node or a Write node.')

	if error == False:
		folderPath = selectedNodeFilePath[ : selectedNodeFilePath.rfind('/') ]
		launch(folderPath)


# File menu browseDir
def browseDir(action):

	if (nuke.root().name() == 'Root') and (action != 'Path'):
		nuke.message('You need to save the Nuke script first!')
	
	else:
		
		# Get full path to script
		scriptPath = nuke.callbacks.filenameFilter( nuke.root().name() )

		# Divide up the paths
		scriptPathSplitted = str.split( scriptPath, '/' )

		# Reset
		openMe = ''

		if action == 'scripts':
			for i in range(0, (len(scriptPathSplitted)-1) ):
				openMe = openMe + scriptPathSplitted[i] + '/'

		elif action == 'sequence':
			for i in range(0, (len(scriptPathSplitted)-4) ):
				openMe = openMe + scriptPathSplitted[i] + '/'

		elif action == 'shot':
			for i in range(0, (len(scriptPathSplitted)-3) ):
				openMe = openMe + scriptPathSplitted[i] + '/'
		
		launch(openMe)
