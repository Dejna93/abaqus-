from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='GoatSoft',
                                 moduleName='goatsoftgui',
                                 functionName='start_app()',
                                 author='koza',
                                 description='First gui version')
