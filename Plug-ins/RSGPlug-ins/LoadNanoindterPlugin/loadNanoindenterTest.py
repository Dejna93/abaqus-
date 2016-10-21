from abaqus import *
from abaqusConstants import *


def loadmaterials(indenter):

    if (indenter == 'indenterKulka'):

        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                     sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        s1.FixedConstraint(entity=g[2])
        s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(-5.0, 0.0), point2=(0.0, 5.0),
                           direction=CLOCKWISE)
        s1.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
        s1.CoincidentConstraint(entity1=v[1], entity2=g[2], addUndoState=False)
        s1.Line(point1=(-5.0, 0.0), point2=(0.0, 0.0))
        s1.HorizontalConstraint(entity=g[4], addUndoState=False)
        s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
        s1.Line(point1=(0.0, 0.0), point2=(0.0, 5.0))
        s1.VerticalConstraint(entity=g[5], addUndoState=False)
        s1.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
        p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                                       type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-1']
        p.BaseSolidRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']

    mdb.models['Model-1'].Material('Titanium')
    mdb.models['Model-1'].materials['Titanium'].Density(table=((4500,),))
    mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3),))

    mdb.models['Model-1'].Material('AISI 1005 Steel')
    mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872,),))
    mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29),))

    mdb.models['Model-1'].Material('Gold')
    mdb.models['Model-1'].materials['Gold'].Density(table=((19320,),))
    mdb.models['Model-1'].materials['Gold'].Elastic(table=((77.2E9, 0.42),))
