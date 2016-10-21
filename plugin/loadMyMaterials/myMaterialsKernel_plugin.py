from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerKernelMenuButton(buttonText='Load MyMaterials Plug-in',
                                 moduleName='loadMyMaterialsKernelScript',
                                 functionName='loadmaterials()',
                                 author='student',
                                 description='My First plug-in')
