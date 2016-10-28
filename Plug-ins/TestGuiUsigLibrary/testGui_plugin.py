from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='testGui',
                                 moduleName='testGui',
                                 functionName='testFunction()',
                                 author='student',
                                 description='My First plug-in')
