import maya.cmds as mc

class MirrorWindow(object):
    
    def __init__(self):
        self.window="myWindow"
        self.title = "Mirror Object"
        self.size = (350, 100)
        self.axis = "x"
        self.isWorld = True
        self.isPivotCentered = True
        
        if mc.window("myWindow", exists=True):
            mc.deleteUI("myWindow", window=True)
         
        window = mc.window("myWindow", title="Mirror Object", widthHeight=(400, 100), sizeable = False)
        # Create a layout for the radio buttons on the same line
        
        column_layout = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 5), rowSpacing=5)
        row_layout = mc.rowLayout(numberOfColumns=4, columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)],
                                        columnWidth=[(1, 200), (2, 50), (3, 50), (4, 50)])
        label = mc.text(label="Mirror object along axis", align="center", font="boldLabelFont")
        radio_collection = mc.radioCollection()
        mc.radioButton(label="X", onCommand=lambda *args: self.assignaxis("x"), collection=radio_collection)
        mc.radioButton(label="Y", onCommand=lambda *args: self.assignaxis("y"), collection=radio_collection)
        mc.radioButton(label="Z", onCommand=lambda *args: self.assignaxis("z"), collection=radio_collection)
        
        mc.setParent('..')  # Return to the main layout
        row_layout = mc.rowLayout(numberOfColumns=3, columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)],
                                        columnWidth=[(1, 100), (2, 100), (3,100)])
        label = mc.text(label=" ", align="center", font="boldLabelFont")
        new_radio_collection = mc.radioCollection()
        mc.radioButton(label="World", onCommand=lambda *args: self.assignWorldorObject(True), collection=new_radio_collection)
        mc.radioButton(label="Object", onCommand=lambda *args: self.assignWorldorObject(False), collection=new_radio_collection)
        
        mc.setParent('..')  # Return to the main layout
        row_layout = mc.rowLayout(numberOfColumns=2, columnAttach=[(1, 'both', 0), (2, 'both', 0)],
                                        columnWidth=[(1, 100), (2, 200)])
        label = mc.text(label="", align="left", font="boldLabelFont")
        mc.checkBox(label="Center pivot after mirroring", changeCommand=self.assignPivot)
        
        mc.setParent('..')
        button_command = lambda *args: self.mirror_object(self.axis, self.isWorld, self.isPivotCentered)
        mc.button(label = "Mirror", command = button_command)
        mc.showWindow(window)
        
    def assignaxis(self, axis):
        print("assigned", axis)
        self.axis= axis
        
    def assignWorldorObject(self, isWorld):
        print(isWorld)
        self.isWorld = isWorld
        

    def assignPivot(self, state):
        self.isPivotCentered = bool(state)
        print(self.isPivotCentered)
        
    def mirror_object(self, axis, isWorld, centerPivot):
        selected = mc.ls(sl=1)
        if len(selected) == 0:
            mc.warning("please select an object")
        if axis == "x":
            for selection in selected:
                mc.makeIdentity(apply=True,t=1, r=1, s=1, n=0, pn = 1)  
                duplicated = mc.duplicate(selection)[0]
                if isWorld:
                    mc.scale(-1, 1, 1, selection, relative=True, pivot=(0, 0, 0))
                else:
                    mc.scale(-1, 1, 1, selection, relative=True, objectCenterPivot = True)
                mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn = 1)
                
                if centerPivot:
                    mc.xform(selection, cp = 1)
                    mc.xform(duplicated, cp = 1)
        elif axis == "y":
            for selection in selected:
                mc.makeIdentity(apply=True,t=1, r=1, s=1, n=0, pn = 1)  
                duplicated = mc.duplicate(selection)[0]
                if isWorld:
                    mc.scale(1, -1, 1, selection, relative=True, pivot=(0, 0, 0))
                else:
                    mc.scale(1, -1, 1, selection, relative=True, objectCenterPivot = True)
                mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn = 1)
                
                if centerPivot:
                    mc.xform(selection, cp = 1)
                    mc.xform(duplicated, cp = 1)
            
        else:
            
            for selection in selected:
                
                mc.makeIdentity(apply=True,t=1, r=1, s=1, n=0, pn = 1)  
                duplicated = mc.duplicate(selection)[0]
                if isWorld:
                    mc.scale(1, 1, -1, selection, relative=True, pivot=(0, 0, 0))
                else:
                    mc.scale(1, 1, -1, selection, relative=True, objectCenterPivot = True)
                mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn = 1)
                
                if centerPivot:
                    mc.xform(selection, cp = 1)
                    mc.xform(duplicated, cp = 1)
           
window = MirrorWindow()