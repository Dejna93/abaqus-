from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='GoatSoft',
                                 moduleName='goatsoftgui',
                                 functionName='run_gui()',
                                 author='koza',
                                 description='First gui version')
