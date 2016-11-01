from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='testGui2',
                                 moduleName='testGui',
                                 functionName='testFunction()',
                                 author='student',
                                 description='My First plug-in')
