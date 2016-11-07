from abaqus import *
from abaqusConstants import *

import abaqusCommands


class ActualAbaqusCommands(abaqusCommands.AbaqusCommands):
    def __init__(self):
        pass

    def setindenter(self, indenter,roundingradius=0):
        if indenter == "spherical":
            s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                        sheetSize=200.0)
            g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
            s.setPrimaryObject(option=STANDALONE)
            s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
            s.FixedConstraint(entity=g[2])
            s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-5.0, 0.0), point2=(0.0, 5.0),
                              direction=CLOCKWISE)
            s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
            s.CoincidentConstraint(entity1=v[1], entity2=g[2], addUndoState=False)
            p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                                           type=DISCRETE_RIGID_SURFACE)
            p = mdb.models['Model-1'].parts['Part-1']
            p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
            s.unsetPrimaryObject()
            p = mdb.models['Model-1'].parts['Part-1']
            session.viewports['Viewport: 1'].setValues(displayedObject=p)
            del mdb.models['Model-1'].sketches['__profile__']

        elif indenter == "Vickers":
            s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                        sheetSize=200.0)
            g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
            s.setPrimaryObject(option=STANDALONE)
            s.rectangle(point1=(-5.0, 5.0), point2=(5.0, -5.0))
            p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                                           type=DISCRETE_RIGID_SURFACE)
            p = mdb.models['Model-1'].parts['Part-1']
            p.BaseShellExtrude(sketch=s, depth=20.0, draftAngle=68.0)
            s.unsetPrimaryObject()
            p = mdb.models['Model-1'].parts['Part-1']
            e = p.edges
            if roundingradius > 0:
                e = p.edges
                p.Round(radius=roundingradius, edgeList=(e[0], e[1], e[3], e[5]))
            session.viewports['Viewport: 1'].setValues(displayedObject=p)
            del mdb.models['Model-1'].sketches['__profile__']
        elif indenter == "Berkovich":
            s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                         sheetSize=200.0)
            g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
            s1.setPrimaryObject(option=STANDALONE)
            s1.Line(point1=(-5.0, 0.0), point2=(5.0, 0.0))
            s1.HorizontalConstraint(entity=g[2], addUndoState=False)
            s1.Line(point1=(5.0, 0.0), point2=(0.0, 8.660254))
            s1.Line(point1=(0.0, 8.660254), point2=(-5.0, 0.0))
            p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                                           type=DISCRETE_RIGID_SURFACE)
            p = mdb.models['Model-1'].parts['Part-1']
            p.BaseShellExtrude(sketch=s1, depth=20.0, draftAngle=65.3)
            s1.unsetPrimaryObject()
            p = mdb.models['Model-1'].parts['Part-1']
            if roundingradius > 0:
                e1 = p.edges
                p.Round(radius=roundingradius, edgeList=(e1[0], e1[1], e1[3]))
            session.viewports['Viewport: 1'].setValues(displayedObject=p)
            del mdb.models['Model-1'].sketches['__profile__']


