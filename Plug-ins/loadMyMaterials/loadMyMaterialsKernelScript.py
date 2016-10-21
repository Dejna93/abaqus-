from abaqus import *
from abaqusConstants import *

def loadmaterials():

    mdb.models['Model-1'].Material('Titanium')
    mdb.models['Model-1'].materials['Titanium'].Density(table=((4500, ), ))
    mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3), ))

    mdb.models['Model-1'].Material('AISI 1005 Steel')
    mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872, ), ))
    mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29), ))

    mdb.models['Model-1'].Material('Gold')
    mdb.models['Model-1'].materials['Gold'].Density(table=((19320, ), ))
    mdb.models['Model-1'].materials['Gold'].Elastic(table=((77.2E9, 0.42), ))
