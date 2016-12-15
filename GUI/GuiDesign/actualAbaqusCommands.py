from abaqus import *
from abaqusConstants import *

import abaqusCommands


class ActualAbaqusCommands(abaqusCommands.AbaqusCommands):
    def __init__(self):
        self.specimenWidth = 10.0; self.specimenLength = 10.0; self.specimenHeight = 10.0
        self.a = 5.0; self.sin60 = 0.866025404; self.tan68 = 2.475086853; self.tan60 = 1.732050808;
        self.sphericalRadius = 5.0; self.tan30 = 0.577350269; self.tan65_3 = 2.174155933;
        self.distanceBetweenSpecimenAndIndenter = 0.1; self.indenter = "";

    def setindenter(self, indenter, roundingradius=0, sphericalradius=5):
        try:
            roundingradius = float(roundingradius)
        except ValueError:
            roundingradius = 0.0
        try:
            self.sphericalRadius = float(sphericalradius)
        except ValueError:
            pass
        self.indenter = indenter
        if indenter == "spherical":
            s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                        sheetSize=200.0)
            g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
            s.setPrimaryObject(option=STANDALONE)
            s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
            s.FixedConstraint(entity=g[2])
            s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-1*self.sphericalRadius, 0.0), point2=(0.0, self.sphericalRadius),
                              direction=CLOCKWISE) # przeciwlegle punkty na okregu to -5,0,0 i 5,0,0
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
            s.rectangle(point1=(-self.a/4, self.a/4), point2=(self.a/4, -self.a/4))
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
            s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                         sheetSize=200.0)
            g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
            s1.setPrimaryObject(option=STANDALONE)
            s1.Line(point1=(-self.a/4, 0.0), point2=(self.a/4, 0.0))
            s1.HorizontalConstraint(entity=g[2], addUndoState=False)
            s1.Line(point1=(self.a/4, 0.0), point2=(0.0, (self.a/4)*2*self.sin60))
            s1.Line(point1=(0.0, (self.a/4)*2*self.sin60), point2=(-self.a/4, 0.0))
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
        self.specimenWidth = width; self.specimenHeight = height; self.specimenLength = length
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

    def createBasis(self):
        if self.specimenHeight > self.specimenWidth:
            self.a = self.specimenHeight*2
        else:
            self.a = self.specimenWidth*2
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                     sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.Line(point1=(-0.5*self.a, 0.0), point2=(0.5*self.a, 0.0))
        s1.HorizontalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models['Model-1'].Part(name='Basis', dimensionality=THREE_D,
                                       type=ANALYTIC_RIGID_SURFACE)
        p = mdb.models['Model-1'].parts['Basis']
        p.AnalyticRigidSurfExtrude(sketch=s1, depth=self.a)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Basis']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']

    def rotateSpecimen(self):
        pass

    def prepareAssembly(self):
        a1 = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Basis']
        a1.Instance(name='Basis-1', part=p, dependent=ON)
        a1 = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Indenter']
        a1.Instance(name='Indenter-1', part=p, dependent=ON)
        a1 = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Specimen']
        a1.Instance(name='Specimen-1', part=p, dependent=ON)

    def rotateSpecimen(self):
        a = mdb.models['Model-1'].rootAssembly
        a.rotate(instanceList=('Specimen-1',), axisPoint=(10.0, 0.0, 0.0),
                 axisDirection=(-20.0, 0.0, 0.0), angle=90.0)
        if self.indenter == "spherical":
            self.positionSpherical()
        elif self.indenter == "Vickers":
            self.positionVickers()
        elif self.indenter == "Berkovich":
            self.positionBerkovich()

    def positionSpherical(self):
        a = mdb.models['Model-1'].rootAssembly
        a.rotate(instanceList=('Indenter-1',), axisPoint=(10.0, 0.0, 0.0),
                 axisDirection=(-20.0, 0.0, 0.0), angle=180.0)
        a = mdb.models['Model-1'].rootAssembly
        try:
            tmp = float(self.sphericalRadius + self.specimenHeight + self.distanceBetweenSpecimenAndIndenter)
        except ValueError:
            print('one of the following cannot be converted to float: sphericalRadius, specimenHeight,'
                  ' or distanceBetweenSpicmenAndIndenter')
        a.translate(instanceList=('Indenter-1',), vector=(0.0, tmp, 0.0))

    def positionVickers(self):
        a = mdb.models['Model-1'].rootAssembly
        a.rotate(instanceList=('Indenter-1',), axisPoint=(10.0, 0.0, 0.0),
                 axisDirection=(-20.0, 0.0, 0.0), angle=-90.0)
        a = mdb.models['Model-1'].rootAssembly
        try:
            tmp = float(((self.a/4)/self.tan68) + self.specimenHeight + self.distanceBetweenSpecimenAndIndenter)
        except ValueError:
            print('one of the following cannot be converted to float: sphericalRadius, specimenHeight,'
                  ' or distanceBetweenSpicmenAndIndenter')
        a.translate(instanceList=('Indenter-1',), vector=(0.0, tmp, 0.0))

    def positionBerkovich(self):
        a = mdb.models['Model-1'].rootAssembly
        a.rotate(instanceList=('Indenter-1',), axisPoint=(10.0, 0.0, 0.0),
                 axisDirection=(-20.0, 0.0, 0.0), angle=-90.0)
        a = mdb.models['Model-1'].rootAssembly
        a.translate(instanceList=('Indenter-1',), vector=(0.0, 0.0, -((self.a/4)/self.tan30)/3))
        try:
            tmp = float(((((self.a/4)/self.tan30)/3) / self.tan65_3) + self.specimenHeight + self.distanceBetweenSpecimenAndIndenter)
        except ValueError:
            print('one of the following cannot be converted to float: sphericalRadius, specimenHeight,'
                  ' or distanceBetweenSpicmenAndIndenter')
        a.translate(instanceList=('Indenter-1',), vector=(0.0, tmp, 0.0))
