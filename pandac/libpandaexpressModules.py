from extension_native_helpers import *
Dtool_PreloadDLL("libpandaexpress")
from libpandaexpress import *

from extension_native_helpers import *
Dtool_PreloadDLL("libpandaexpress")
from libpandaexpress import *

"""
Ramfile_extensions module: contains methods to extend functionality
of the Ramfile class
"""

def readlines(self):
    """Reads all the lines at once and returns a list."""
    lines = []
    line = self.readline()
    while line:
        lines.append(line)
        line = self.readline()
    return lines

Dtool_funcToMethod(readlines, Ramfile)
del readlines    

from extension_native_helpers import *
Dtool_PreloadDLL("libpandaexpress")
from libpandaexpress import *

"""
StreamReader_extensions module: contains methods to extend functionality
of the StreamReader class
"""

def readlines(self):
    """Reads all the lines at once and returns a list."""
    lines = []
    line = self.readline()
    while line:
        lines.append(line)
        line = self.readline()
    return lines
    
Dtool_funcToMethod(readlines, StreamReader)        
del readlines

from extension_native_helpers import *
Dtool_PreloadDLL("libpandaexpress")
from libpandaexpress import *

####################################################################
#Dtool_funcToMethod(func, class)        
#del func
#####################################################################

"""
HTTPChannel-extensions module: contains methods to extend functionality
of the HTTPChannel class
"""

def spawnTask(self, name = None, callback = None, extraArgs = []):
        """Spawns a task to service the download recently requested
        via beginGetDocument(), etc., and/or downloadToFile() or
        downloadToRam().  If a callback is specified, that function is
        called when the download is complete, passing in the extraArgs
        given.

        Returns the newly-spawned task.
        """
        if not name:
            name = self.getUrl().cStr()
        from direct.task import Task
        task = Task.Task(self.doTask)
        task.callback = callback
        task.callbackArgs = extraArgs
        return taskMgr.add(task, name)    
Dtool_funcToMethod(spawnTask, HTTPChannel)        
del spawnTask
#####################################################################
        
def doTask(self, task):
        from direct.task import Task
        if self.run():
            return Task.cont
        if task.callback:
            task.callback(*task.callbackArgs)
        return Task.done
    
Dtool_funcToMethod(doTask, HTTPChannel)        
del doTask
#####################################################################

