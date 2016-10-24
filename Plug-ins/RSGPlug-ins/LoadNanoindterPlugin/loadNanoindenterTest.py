"""
    I do not guarantee the correctness of this commentary, thus it is based only on my personal analysis of the code.

    This file is the Kernel module, it holds the fucntion called when the OK button is pressed.

"""

from abaqus import *
from abaqusConstants import *


def loadmaterials(indenter):

    if (indenter == 'spherical'):

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
    elif (indenter == 'Berkovich'):
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                    sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=182.257,
                                                        farPlane=194.866, width=55.6457, height=29.4366,
                                                        cameraPosition=(
                                                            -0.660534, -0.0390082, 188.562),
                                                        cameraTarget=(-0.660534, -0.0390082,
                                                                      0))
        s.Line(point1=(-5.0, 0.0), point2=(5.0, 0.0))
        s.HorizontalConstraint(entity=g[2], addUndoState=False)
        s.Line(point1=(5.0, 0.0), point2=(0.0, 8.660254))
        s.Line(point1=(0.0, 8.660254), point2=(-5.0, 0.0))
        p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                                       type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-1']
        p.BaseSolidExtrude(sketch=s, depth=10.8558, draftAngle=-65.27)
        s.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']
        p = mdb.models['Model-1'].parts['Part-1']
        e1 = p.edges
        p.Round(radius=0.1, edgeList=(e1[0], e1[1], e1[3]))
    elif (indenter == 'Vickers'):
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                    sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(-5.0, 5.0), point2=(5.0, -5.0))
        p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                                       type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-1']
        p.BaseSolidExtrude(sketch=s, depth=2.020131, draftAngle=-68.0)
        s.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']
        p = mdb.models['Model-1'].parts['Part-1']
        e = p.edges
        p.Round(radius=0.1, edgeList=(e[0], e[1], e[3], e[5]))


    mdb.models['Model-1'].Material('Titanium')
    mdb.models['Model-1'].materials['Titanium'].Density(table=((4500,),))
    mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3),))

    mdb.models['Model-1'].Material('AISI 1005 Steel')
    mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872,),))
    mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29),))

    mdb.models['Model-1'].Material('Gold')
    mdb.models['Model-1'].materials['Gold'].Density(table=((19320,),))
    mdb.models['Model-1'].materials['Gold'].Elastic(table=((77.2E9, 0.42),))
