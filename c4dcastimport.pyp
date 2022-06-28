"""		ID LAYOUT

0 - Primary UI
	50 - Header Image
	100 - Group (Program Information)
		101 - Version info
		102 - Description
		103 - Author
		104 - Website
	200 - Group (File Info)
		201 - No Frames
		202 - Framerate
		203 - Time in secs
	300 - Group (Export Options)
		300 - Group (Mode Group)
			300 - Mode Text
			301 - Mode
				302 - -Z Up (Maps)
				303 - +Y Up (default CamIO Import)
		325 - Group (buttons)
			326 - Export btn
			327 - Close btn

"""

# Imports
from itertools import islice
import struct
import c4d
from c4d import plugins
from c4d import documents
from c4d import gui
from c4d import storage
from cast import Cast, Model, Animation, Curve, NotificationTrack, Mesh, Skeleton, Bone, Material, File
import math

# Global Vars
PLUGIN_VERSION_MAJOR = 1
PLUGIN_VERSION_MINOR = 1
PLUGIN_VERSION_STR = "v{}.{}".format(
    PLUGIN_VERSION_MAJOR, PLUGIN_VERSION_MINOR)
PLUGIN_NAME = "Cast Importer " + PLUGIN_VERSION_STR
PLUGIN_DESCRIPTION = "Imports Cast files ."
PLUGIN_ID = 1059545  # Registered Plugin ID
PLUGIN_WEBPAGE = "http://github.com/AllusiveWheat"


def DoWork():

    c4d.StopAllThreads()

    # Select File Name/Loc
    filepath = storage.LoadDialog(
        c4d.FILESELECTTYPE_ANYTHING,
        "Select Cast File ... (*.cast)",
        c4d.FILESELECT_LOAD,
        force_suffix="cast")
    if(filepath is None):  # catch cancel
        return False

    # If the file is not a .cast file, return
    if(filepath.lower().endswith(".cast") == False):
        gui.MessageDialog("File is not a .cast file.")
        return False

    importCast(filepath)
    # Vars

    # Console
    c4d.StatusClear()

    gui.MessageDialog("Successfully Imported Cast File: {}".format(filepath))
    return True

# Banner Definition


def importRootNode(node, path):
    for child in node.ChildrenOfType(Model):
        print("Model: ", child)
        importModelNode(child, path)
    print("Loaded Cast File: {}".format(path))


def importSkeletonNode(skeleton):
    if skeleton is None:
        return (None, None)

    bones = skeleton.Bones()
    


def importModelNode(model, path):
    # Create null object
    CurrentProj = documents.GetActiveDocument()

    meshes = model.Meshes()

    for mesh in meshes:
        vertexCount = mesh.VertexCount()
        print("Vertex Count: ", vertexCount)
        facecount = mesh.FaceCount()
        polyCount = mesh.VertexCount()
        if polyCount != 0:
            polyObj = c4d.PolygonObject(vertexCount *3, vertexCount)
            polyObj.SetName(mesh.Name())
            #Fill the polygon object with the mesh data
            #Create a new c4d.Vector for each vertex
            for i in range(int(vertexCount)):
                v = mesh.VertexPositionBuffer()
                array = list(v)
                
                # Split is steped by 3 because each vertex is a 3d vector
                split = [array[i:i+3] for i in range(0, len(array), 3)]
                #Convert split into a tuple
                allPos = tuple(split)
                #Convert tuple into a list
                posList = list(allPos)
                
                print("PosList: ", posList[0])
                
                
                
                
                
                
               # polyObj.SetPoint(i, c4d.Vector(v.x, v.y, v.z))
            CurrentProj.InsertObject(polyObj)


def importCast(path):
    cast = Cast()
    if cast.load(path) == False:
        print("Failed to load Cast file: {}".format(path))

        # Import Cast File
    for root in cast.Roots():
        importRootNode(root, path)

# UI Definition


class PrimaryUI(gui.GeDialog):

    # Layout Design
    def CreateLayout(self):
        CurrentProj = documents.GetActiveDocument()
        self.SetTitle(PLUGIN_NAME)

        self.GroupBegin(100, c4d.BFH_SCALE, 1, 4)  # PROGRAM INFO GROUP

        self.AddStaticText(101, c4d.BFH_RIGHT, 0, 0, PLUGIN_VERSION_STR)
        self.AddStaticText(102, c4d.BFH_CENTER, 0, 0, PLUGIN_DESCRIPTION)
        self.AddStaticText(103, c4d.BFH_CENTER, 0, 0,
                           "Plugin by AllusiveWheat")
        self.AddStaticText(104, c4d.BFH_CENTER, 0, 0, PLUGIN_WEBPAGE)

        self.GroupEnd()

        self.AddStaticText(0, c4d.BFH_CENTER, 0, 3)  # spacer
        self.AddSeparatorH(300, c4d.BFH_CENTER)
        self.AddStaticText(0, c4d.BFH_CENTER, 0, 3)  # spacer

        self.AddStaticText(0, c4d.BFH_CENTER, 0, 4)  # spacer

        self.GroupBegin(300, c4d.BFH_SCALE, 1, 3)  # Mode and Buttons

        self.AddStaticText(0, c4d.BFH_CENTER, 0, 4)  # spacer

        self.GroupBegin(325, c4d.BFH_SCALE, 2, 1)

        self.AddButton(326, c4d.BFH_LEFT, 80, 16, "Import")
        self.AddButton(327, c4d.BFH_RIGHT, 80, 16, "Close")

        self.GroupEnd()
        self.GroupEnd()

        return True

    # USER CONTROL SECTION
    def Command(self, id, msg):

        if(id == 327):  # Close Btn
            self.Close()
            return True

        if(id == 326):  # Export Btn
            if(DoWork()):
                self.Close()
                return True

            return False

        return True


# Plugin Definition
class C4DCam2HLAECamIO(plugins.CommandData):

    def Execute(self, BaseDocument):
        # defines what happens when the user clicks the plugin in the menu
        UI = PrimaryUI(gui.GeDialog)
        UI.Open(c4d.DLG_TYPE_MODAL, PLUGIN_ID, -1, -1, 400, 360, 0)  # open ui

        return True

# Main Definition


def main():
    # Icon
    icon = c4d.bitmaps.BaseBitmap()
    iconpath = __file__
    iconpath = iconpath.replace("c4dcastimport.pyp", "")  # remove plugin name
    iconpath += "res\\icon.png"
    icon.InitWith(iconpath)

    # Register the plugin
    plugins.RegisterCommandPlugin(
        PLUGIN_ID,
        PLUGIN_NAME,
        0,
        icon,
        PLUGIN_DESCRIPTION,
        C4DCam2HLAECamIO())

    # Console confirmation
    print("Loaded %s" % (PLUGIN_NAME))


# Main Execution
main()
