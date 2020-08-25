from extension_native_helpers import *
Dtool_PreloadDLL("libpandaode")
from libpandaode import *

from extension_native_helpers import *
Dtool_PreloadDLL("libpanda")
from libpanda import *

####################################################################
#Dtool_funcToMethod(func, class)
#del func
#####################################################################

"""
OdeGeom-extensions module: contains methods to extend functionality
of the OdeGeom class
"""

def convert(self):
    """
    Do a sort of pseudo-downcast on this geom in 
    order to expose its specialized functions.
    """
    if self.getClass() == OdeGeom.GCSphere:
        return self.convertToSphere()
    elif self.getClass() == OdeGeom.GCBox:
        return self.convertToBox()
    elif self.getClass() == OdeGeom.GCCappedCylinder:
        return self.convertToCappedCylinder()
    elif self.getClass() == OdeGeom.GCPlane:
        return self.convertToPlane()
    elif self.getClass() == OdeGeom.GCRay:
        return self.convertToRay()
    # elif self.getClass() == OdeGeom.GCConvex:
    #     return self.convertToConvex()
    # elif self.getClass() == OdeGeom.GCGeomTransform:
    #     return self.convertToGeomTransform()
    elif self.getClass() == OdeGeom.GCTriMesh:
        return self.convertToTriMesh()
    # elif self.getClass() == OdeGeom.GCHeightfield:
    #     return self.convertToHeightfield()
    elif self.getClass() == OdeGeom.GCSimpleSpace:
        return self.convertToSimpleSpace()
    elif self.getClass() == OdeGeom.GCHashSpace:
        return self.convertToHashSpace()
    elif self.getClass() == OdeGeom.GCQuadTreeSpace:
        return self.convertToQuadTreeSpace()
Dtool_funcToMethod(convert, OdeGeom)
del convert

def getConvertedSpace(self):
    """
    """
    return self.getSpace().convert()
Dtool_funcToMethod(getConvertedSpace, OdeGeom)
del getConvertedSpace

def getAABounds(self):
    """
    A more Pythonic way of calling getAABB()
    """
    min = Point3()
    max = Point3()
    self.getAABB(min,max)
    return min,max
Dtool_funcToMethod(getAABounds, OdeGeom)
del getAABounds


from extension_native_helpers import *
Dtool_PreloadDLL("libpanda")
from libpanda import *

####################################################################
#Dtool_funcToMethod(func, class)
#del func
#####################################################################

"""
OdeSpace-extensions module: contains methods to extend functionality
of the OdeSpace classe
"""

def convert(self):
    """
    Do a sort of pseudo-downcast on this space in 
    order to expose its specialized functions.
    """
    if self.getClass() == OdeGeom.GCSimpleSpace:
        return self.convertToSimpleSpace()
    elif self.getClass() == OdeGeom.GCHashSpace:
        return self.convertToHashSpace()
    elif self.getClass() == OdeGeom.GCQuadTreeSpace:
        return self.convertToQuadTreeSpace()
Dtool_funcToMethod(convert, OdeSpace)
del convert

def getConvertedGeom(self, index):
    """
    Return a downcast geom on this space.
    """
    return self.getGeom(index).convert()
Dtool_funcToMethod(getConvertedGeom, OdeSpace)
del getConvertedGeom

def getConvertedSpace(self):
    """
    """
    return self.getSpace().convert()
Dtool_funcToMethod(getConvertedSpace, OdeSpace)
del getConvertedSpace

def getAABounds(self):
    """
    A more Pythonic way of calling getAABB()
    """
    min = Point3()
    max = Point3()
    self.getAABB(min,max)
    return min,max
Dtool_funcToMethod(getAABounds, OdeSpace)
del getAABounds


from extension_native_helpers import *
Dtool_PreloadDLL("libpanda")
from libpanda import *

####################################################################
#Dtool_funcToMethod(func, class)
#del func
#####################################################################

"""
OdeJoint-extensions module: contains methods to extend functionality
of the OdeJoint class
"""

def attach(self, body1, body2):
    """
    Attach two bodies together.
    If either body is None, the other will be attached to the environment.
    """
    if body1 and body2:
        self.attachBodies(body1, body2)
    elif body1 and not body2:
        self.attachBody(body1, 0)
    elif not body1 and body2:
        self.attachBody(body2, 1)
Dtool_funcToMethod(attach, OdeJoint)
del attach

def convert(self):
    """
    Do a sort of pseudo-downcast on this joint in 
    order to expose its specialized functions.
    """
    if self.getJointType() == OdeJoint.JTBall:
        return self.convertToBall()
    elif self.getJointType() == OdeJoint.JTHinge:
        return self.convertToHinge()
    elif self.getJointType() == OdeJoint.JTSlider:
        return self.convertToSlider()
    elif self.getJointType() == OdeJoint.JTContact:
        return self.convertToContact()
    elif self.getJointType() == OdeJoint.JTUniversal:
        return self.convertToUniversal()
    elif self.getJointType() == OdeJoint.JTHinge2:
        return self.convertToHinge2()
    elif self.getJointType() == OdeJoint.JTFixed:
        return self.convertToFixed()
    elif self.getJointType() == OdeJoint.JTNull:
        return self.convertToNull()
    elif self.getJointType() == OdeJoint.JTAMotor:
        return self.convertToAMotor()
    elif self.getJointType() == OdeJoint.JTLMotor:
        return self.convertToLMotor()
    elif self.getJointType() == OdeJoint.JTPlane2d:
        return self.convertToPlane2d()
Dtool_funcToMethod(convert, OdeJoint)
del convert


from extension_native_helpers import *
Dtool_PreloadDLL("libpanda")
from libpanda import *

####################################################################
#Dtool_funcToMethod(func, class)
#del func
#####################################################################

"""
OdeBody-extensions module: contains methods to extend functionality
of the OdeBody classe
"""

def getConvertedJoint(self, index):
    """
    Return a downcast joint on this body.
    """
    return self.getJoint(index).convert()
Dtool_funcToMethod(getConvertedJoint, OdeBody)
del getConvertedJoint


