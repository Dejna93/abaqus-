"""
    I do not guarantee the correctness of this commentary, thus it is based only on my personal analysis of the code.


    This is the file that starts the plug in
    buttonText holds the text from the button in plug-ins menu in abaqus
    loadNanoindterPluginDB.py is the file that defines the gui elements and holds the KernelScript name which is called when
    confirm button is clicked in RSGPlugin.
    kernelInitString imports the file with definition of the kernel function.

"""
from abaqusGui import getAFXApp, Activator, AFXMode
from abaqusConstants import ALL
import os
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='NonoindenterAlpha', 
    object=Activator(os.path.join(thisDir, 'loadNanoindterPluginDB.py')),
    kernelInitString='import loadNanoindenterTest',
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
