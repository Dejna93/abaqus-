from abaqusGui import AFXApp
import sys

from customCaeMainWindow import CustomCaeMainWindow

app = AFXApp(appName='ABAQUS/CAE',
             vendorName='ABAQUS, Inc.',
             productName='',
             majorNumber=1,
             minorNumber=1,
             updateNumber=1,
             prerelease=False)
app.init(sys.argv)

customCaeMainWindow(app)
app.create()
app.run()