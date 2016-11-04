from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='GUIexample',
                                 moduleName='GUIexample',
                                 functionName='testFunction()',
                                 author='student',
                                 description='My First plug-in')