bl_info = {
    "name": "Color Fix",
    "blender": (4, 00, 0),
    "category": "Color"
}


import bpy


#Getting the color for the sliders
def get_color_from_base(self, context):
    slider_value = self.accentOne_value
    
    #accent 1
    r = self.color_picker[0] - ((0 + (self.accentOne_value / 100) * (99 - 0)) / 255.0)
    g = self.color_picker[1] - ((38 + (self.accentOne_value / 100) * (92 - 38)) / 255.0)
    b = self.color_picker[2] - ((25 + (self.accentOne_value / 100) * (91 - 25)) / 255.0)
    
    self.accentOne_color = (r, g, b, 1.0)
    
    
    #accent 2
    r = self.color_picker[0] - ((35 + (self.accentTwo_value / 100) * (155 - 35)) / 255.0)
    g = self.color_picker[1] - ((102 + (self.accentTwo_value / 100) * (165 - 102)) / 255.0)
    b = self.color_picker[2] - ((76 + (self.accentTwo_value / 100) * (146 - 76)) / 255.0)
    
    self.accentTwo_color = (r, g, b, 1.0)
    
    
    #highlight
    r = self.color_picker[0] - ((-58 + (self.highlight_value / 100) * (0 - -58)) / 255.0)
    g = self.color_picker[1] - ((-50 + (self.highlight_value / 100) * (0 - -50)) / 255.0)
    b = self.color_picker[2] - ((-42 + (self.highlight_value / 100) * (0 - -42)) / 255.0)
    
    self.highlight_color = (r, g, b, 1.0)
    






class ColorFixUIPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color Fix"
    bl_idname = "OBJECT_PT_ColorFix_ui"
    bl_space_type = 'VIEW_3D'         # Area where the panel will be displayed
    bl_region_type = 'UI'             # Region where the panel will be displayed (UI is the sidebar)
    bl_category = "Color Fix"             # Tab name in the sidebar

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        props = context.scene.colorfix_ui_props
        
        #The object selector
        layout.prop_search(props, "object_selector", context.scene, "objects", text="Object Selector")
        
        #layout.template_ID(props, "object_selector", new="object.new", open="object.open")
        
        
        #Color picker for base color
        layout.prop(props, "color_picker", text="Base Color")
        
        # Slider for Accent 1
        layout.prop(props, "accentOne_value", slider=True)
        
        layout.label(text=f"Slider Value: {props.accentOne_value:.2f}")
        
        #Color preview for accent 1
        layout.prop(props, "accentOne_color", text="Accent 1 Color")
        
        
        # Slider for Accent 2
        layout.prop(props, "accentTwo_value", slider=True)
        
        layout.label(text=f"Slider Value: {props.accentTwo_value:.2f}")
        
        #Color preview for accent 2
        layout.prop(props, "accentTwo_color", text="Accent 2 Color")
        
        
        # Slider for Highlight
        layout.prop(props, "highlight_value", slider=True)
        
        layout.label(text=f"Slider Value: {props.highlight_value:.2f}")
        
        #Color preview for Highlight
        layout.prop(props, "highlight_color", text="Highlight Color")
        
        
        
        # A button that applies the color fix to the material
        layout.operator("wm.color_fix")
        



# Setting the Slider Operation
class ColorFixProperties(bpy.types.PropertyGroup):
    
    object_selector: bpy.props.PointerProperty(
        name="Object Selector",
        type=bpy.types.Object,
        description="Select an object with the correct materia"
    )
    
    
    accentOne_value: bpy.props.FloatProperty(
        name="Accent 1",
        description="Controls Accent 1 Percentage",
        default=0.5,
        min=0.0,
        max=1.0,
        update=get_color_from_base
    )
    
    accentOne_color: bpy.props.FloatVectorProperty(
        name="Accent 1 Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.0, 0.0, 1.0)
    )
    
    accentTwo_value: bpy.props.FloatProperty(
        name="Accent 2",
        description="Controls Accent 1 Percentage",
        default=0.5,
        min=0.0,
        max=1.0,
        update=get_color_from_base
    )
    
    accentTwo_color: bpy.props.FloatVectorProperty(
        name="Accent 2 Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.0, 0.0, 1.0)
    )
    
    highlight_value: bpy.props.FloatProperty(
        name="Highlight",
        description="Controls Accent 1 Percentage",
        default=0.5,
        min=0.0,
        max=1.0,
        update=get_color_from_base
    )
    
    highlight_color: bpy.props.FloatVectorProperty(
        name="Highlight Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.0, 0.0, 1.0)
    )
    
    color_picker: bpy.props.FloatVectorProperty(
        name="Base Color",
        description="Pick a Base Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        update=get_color_from_base
    )
    
# Making the adjustments to the color button press
class WM_OnColorFixPress(bpy.types.Operator):
    bl_label = "Apply Changes"
    bl_idname = "wm.color_fix"
    
    def execute(self, context):
        #obj = bpy.context.active_object
        props = context.scene.colorfix_ui_props
        obj = props.object_selector
        
        if obj is not None:
            
            
            material = obj.active_material
            
            if material and material.use_nodes:
                nodes = material.node_tree.nodes
                color_group_node = None
                
                
                for node in nodes:
                    if node.type == 'GROUP' and node.node_tree is not None and node.node_tree.name == "Cel Shade":
                        color_group_node = node
                        break
                    
                if color_group_node is not None:
                    
                    if 'Base Color' in color_group_node.inputs:
                        
                        color_input = color_group_node.inputs['Base Color']
                        if  len(color_input.default_value) == 4:
                            color_input.default_value = props.color_picker
                    
                    if 'Accent 1' in color_group_node.inputs:
                        
                        color_input = color_group_node.inputs['Accent 1']
                        if  len(color_input.default_value) == 4:
                            color_input.default_value = props.accentOne_color
                            
                    if 'Accent 2' in color_group_node.inputs:
                        
                        color_input = color_group_node.inputs['Accent 2']
                        if  len(color_input.default_value) == 4:
                            color_input.default_value = props.accentTwo_color
                            
                    if 'Highlight' in color_group_node.inputs:
                        
                        color_input = color_group_node.inputs['Highlight']
                        if  len(color_input.default_value) == 4:
                            color_input.default_value = props.highlight_color
        return {'FINISHED'}


# Register the panel and operator
def register():
    bpy.utils.register_class(ColorFixProperties)
    bpy.types.Scene.colorfix_ui_props = bpy.props.PointerProperty(type=ColorFixProperties)
    bpy.utils.register_class(ColorFixUIPanel)
    bpy.utils.register_class(WM_OnColorFixPress)

def unregister():
    bpy.utils.unregister_class(ColorFixUIPanel)
    bpy.utils.unregister_class(ColorFixProperties)
    del bpy.types.Scene.colorfix_ui_props
    bpy.utils.unregister_class(WM_OnColorFixPress)

# Ensure the script registers when run from the text editor
if __name__ == "__main__":
    register()