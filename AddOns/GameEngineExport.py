bl_info = {
    "name": "Export for Game Engines",
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "version": (1, 0, 0),
    "author": "Matthew Wolfe",
    "description": "Exports objects with specific settings for game engines like Unity and Unreal Engine."
}

import bpy
import os




class EXPORT_OT_to_game_engines(bpy.types.Operator):
    bl_idname = "export.to_game_engines"
    bl_label = "Export for Game Engines"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    game_engine: bpy.props.EnumProperty(
        name="Game Engine",
        description="Choose the Game Engine for exporting",
        items=[
            ('UNITY', "Unity", "Export for Unity"),
            ('UNREALENGINE', "Unreal Engine", "Export for Unreal Engine")
        ],
        default='UNITY'
    )
    
    file_format: bpy.props.EnumProperty(
        name="File Format",
        description="Choose the file format for exporting",
        items=[
            ('FBX', "FBX (.fbx)", "Export as FBX format"),
            ('OBJ', "OBJ (.obj)", "Export as OBJ format"),
            ('GLTF', "glTF (.gltf/.glb)", "Export as glTF format")
        ],
        default='FBX'
    )
    
    model_name: bpy.props.StringProperty(
        name="Model Name",
        description="Name of the exported model",
        default="exported_model"
    )
    
    folder_path: bpy.props.StringProperty(
        name="Folder Path",
        description="Select the folder path to export to",
        subtype='DI_PATH',
        default=""    
    )
    
    def draw(self, context):
        layout = self.layout
        
        
        
        
        #Main Settings
        layout.separator()
        layout.label(text="Select Game Engine:")
        layout.prop(self, "game_engine")
        layout.label(text="Select File Format:")
        layout.prop(self, "file_format")
        
        #Naming
        layout.label(text="Model Name:")
        layout.prop(self, "model_name")
        
        #Folder path selection
        row = layout.row()
        row.prop(self, "folder_path", text="")
        row.operator("export.select_folder", text="Select Folder", icon='FILE_FOLDER')
        
        
        layout.label(text="Export:")
        
        
        
    
    
    

    def execute(self, context):
        
        folder_path = context.window_manager.export_folder_path
        
        file_format = self.file_format
        
        game_engine = self.game_engine
        
        file_name = self.model_name
        
        full_path = os.path.join(folder_path, f"{file_name}.{file_format.lower()}")
        
        #Perform the exporting here
        
        #Settings for Game Engine
        
        axis_forward = '-Z'
        axis_up = 'Y'
        
        if game_engine == 'UNITY':
            axis_forward = '-Z'
            axis_up = 'Y'
            
        elif game_engine == 'UNREALENGINE':
            axis_forward = 'X'
            axis_up = 'Z'
        
        #Settings for File Format
        
        if file_format == 'FBX':
            bpy.ops.export_scene.fbx(
                filepath=full_path,
                use_selection=True,
                apply_unit_scale=True,
                global_scale=1.0,
                axis_forward=axis_forward,
                axis_up=axis_up,
                path_mode='AUTO'
            )
            self.report({'INFO'}, f"Exported to {full_path} as FBX")
            
            
        elif file_format == 'OBJ':
            bpy.ops.export_scene.obj(
                filepath=full_path,
                use_selection=True,
                apply_unit_scale=True,
                global_scale=1.0,
                axis_forward=axis_forward,
                axis_up=axis_up,
                path_mode='AUTO'
            )
            self.report({'INFO'}, f"Exported to {full_path} as OBJ")
            
            
        elif file_format == 'GLTF':
            bpy.ops.export_scene.gltf(
                filepath=full_path,
                export_format='GLB',
                use_selection=True,
                apply_unit_scale=True,
                global_scale=1.0,
                axis_forward=axis_forward,
                axis_up=axis_up,
                path_mode='AUTO'
            )
            self.report({'INFO'}, f"Exported to {full_path} as glTF")
        
        
        
        return {'FINISHED'}

    def invoke(self, context, event):
        # Display the pop-up
        return context.window_manager.invoke_props_dialog(self)
    
class EXPORT_OT_select_folder(bpy.types.Operator):
    bl_idname = "export.select_folder"
    bl_label = "Select Folder"
    
    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        context.window_manager.export_folder_path = self.directory
        
        bpy.ops.export.to_game_engines('INVOKE_DEFAULT')
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    

    
    

def menu_func(self, context):
    self.layout.operator(EXPORT_OT_to_game_engines.bl_idname, text="Export for Game Engines")



def register():
    bpy.utils.register_class(EXPORT_OT_to_game_engines)
    bpy.utils.register_class(EXPORT_OT_select_folder)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)
    
    bpy.types.WindowManager.export_folder_path = bpy.props.StringProperty(name="Export Folder Path")

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_to_game_engines)
    bpy.utils.unregister_class(EXPORT_OT_select_folder)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)
    
    del bpy.types.WindowManager.export_folder_path

if __name__ == "__main__":
    register()
