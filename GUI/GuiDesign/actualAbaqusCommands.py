from abaqus import *
from abaqusConstants import *

import abaqusCommands


class ActualAbaqusCommands(abaqusCommands.AbaqusCommands):
    def __init__(self):
        pass

    def setindenter(self, indenter,roundingradius=0):
        try:
            float(roundingradius)
        except ValueError:
            roundingradius = 0.0
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
            p = mdb.models['Model-1'].Part(name='Indenter', dimensionality=THREE_D,
                                           type=DISCRETE_RIGID_SURFACE)
            p = mdb.models['Model-1'].parts['Indenter']
            p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
            s.unsetPrimaryObject()
            p = mdb.models['Model-1'].parts['Indenter']
            session.viewports['Viewport: 1'].setValues(displayedObject=p)
            del mdb.models['Model-1'].sketches['__profile__']

        elif indenter == "Vickers":
            s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                        sheetSize=200.0)
            g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
            s.setPrimaryObject(option=STANDALONE)
            s.rectangle(point1=(-5.0, 5.0), point2=(5.0, -5.0))
            p = mdb.models['Model-1'].Part(name='Indenter', dimensionality=THREE_D,
                                           type=DISCRETE_RIGID_SURFACE)
            p = mdb.models['Model-1'].parts['Indenter']
            p.BaseShellExtrude(sketch=s, depth=20.0, draftAngle=68.0)
            s.unsetPrimaryObject()
            p = mdb.models['Model-1'].parts['Indenter']
            e = p.edges
            if roundingradius > 0:
                e = p.edges
                p.Round(radius=roundingradius, edgeList=(e[0], e[1], e[3], e[5]))
            session.viewports['Viewport: 1'].setValues(displayedObject=p)
            del mdb.models['Model-1'].sketches['__profile__']
        elif indenter == "Berkovich":
            s1 = mdb.models['Indenter'].ConstrainedSketch(name='__profile__',
                                                         sheetSize=200.0)
            g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
            s1.setPrimaryObject(option=STANDALONE)
            s1.Line(point1=(-5.0, 0.0), point2=(5.0, 0.0))
            s1.HorizontalConstraint(entity=g[2], addUndoState=False)
            s1.Line(point1=(5.0, 0.0), point2=(0.0, 8.660254))
            s1.Line(point1=(0.0, 8.660254), point2=(-5.0, 0.0))
            p = mdb.models['Model-1'].Part(name='Indenter', dimensionality=THREE_D,
                                           type=DISCRETE_RIGID_SURFACE)
            p = mdb.models['Model-1'].parts['Indenter']
            p.BaseShellExtrude(sketch=s1, depth=20.0, draftAngle=65.3)
            s1.unsetPrimaryObject()
            p = mdb.models['Model-1'].parts['Indenter']
            if roundingradius > 0:
                e1 = p.edges
                p.Round(radius=roundingradius, edgeList=(e1[0], e1[1], e1[3]))
            session.viewports['Viewport: 1'].setValues(displayedObject=p)
            del mdb.models['Model-1'].sketches['__profile__']

    def createSpecimen(self, width, length, height):
        try:
            width = float(width)
        except ValueError:
            width = 10.0
        try:
            length = float(length)
        except ValueError:
            length = 10.0
        try:
            height = float(height)
        except ValueError:
            height = 10.0
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                     sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.rectangle(point1=(-width/2, length/2), point2=(length/2, -width/2))
        p = mdb.models['Model-1'].Part(name='Specimen', dimensionality=THREE_D,
                                       type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Specimen']
        p.BaseSolidExtrude(sketch=s1, depth=height)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Specimen']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']

    def createBasis(self, a):
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                     sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.Line(point1=(-0.5*a, 0.0), point2=(0.5*a, 0.0))
        s1.HorizontalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models['Model-1'].Part(name='Basis', dimensionality=THREE_D,
                                       type=ANALYTIC_RIGID_SURFACE)
        p = mdb.models['Model-1'].parts['Basis']
        p.AnalyticRigidSurfExtrude(sketch=s1, depth=a)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Basis']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']
