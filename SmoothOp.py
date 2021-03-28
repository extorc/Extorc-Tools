bl_info = {
    "name": "Extorc Tools",
    "blender": (2, 92, 0),
    "category": "Object",
}

import bpy
from bpy.types import Menu, Operator, Panel
addon_keymaps = []
   
class MirrorOp(Operator):
    """Quick Mirror Operation"""
    bl_idname = "extorctools.mirrorop" 
    bl_label = "Mirror Op"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        cutter = []
        target = bpy.context.active_object
        lis = bpy.context.selected_objects
        for x in range(len(lis)):
            if len(lis) == 1:
                raise Exception("2 Objects must be selected")
            elif not lis[x] == target:
                cutter.append(lis[x])
                break
        new_mod = target.modifiers.new(name = f"mir" , type = 'MIRROR')
        new_mod.mirror_object = cutter[0]
        return {'FINISHED'}
class BoolOp(Operator):
    """Quick Booelan Operation"""
    bl_idname = "extorctools.boolop" 
    bl_label = "Bool Op"    
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        cutter = []
        target = bpy.context.active_object
        lis = bpy.context.selected_objects
        for x in range(len(lis)):
            if len(lis) == 1:
                raise Exception("2 Objects must be selected")
            elif not lis[x] == target:
                cutter.append(lis[x])
                break
        new_mod = target.modifiers.new(name = f"dif" , type = 'BOOLEAN')
        new_mod.object = cutter[0]
        cutter[0].display_type = 'BOUNDS'
        return {'FINISHED'}
class ShadeSmooth(Operator):
    """Shade Smooth and Auto Smooth in one operator""" 
    bl_idname = "extorctools.smoothop" 
    bl_label = "Smooth Op"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True
        return {'FINISHED'}
        
class SubSurfOp(Operator):
    
    """Quick Subdivision Surface""" 
    bl_idname = "extorctools.subsurfop" 
    bl_label = "Subsurf Op"    
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        try:
            bpy.context.object.modifiers["Subdivision"].levels = bpy.context.object.modifiers["Subdivision"].levels + 1
        except:
            bpy.ops.object.modifier_add(type='SUBSURF')
        return {'FINISHED'} 
    
    
class extorc_pie(Menu):
    bl_label = "Extorc Tools"
    bl_idname = "extorctoolspie"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("extorctools.smoothop")
        pie = layout.menu_pie()
        pie.operator("extorctools.subsurfop")
        pie = layout.menu_pie()
        pie.operator("extorctools.boolop")
        pie = layout.menu_pie()
        pie.operator("extorctools.mirrorop")
        
    
class pie_operator(Operator):
    bl_label = "Pie Caller"
    bl_idname = "org.extorctools" 
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="extorctoolspie")
        return {'FINISHED'}

def key_map(operator):
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(operator.bl_idname, 'D', 'PRESS', ctrl=True, shift=False)
    addon_keymaps.append((km, kmi))   
   
def remove_key_map():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
def register():
    bpy.utils.register_class(ShadeSmooth)
    bpy.utils.register_class(extorc_pie)
    bpy.utils.register_class(pie_operator)
    bpy.utils.register_class(SubSurfOp)
    bpy.utils.register_class(BoolOp)
    bpy.utils.register_class(MirrorOp)
    key_map(pie_operator)
    
def unregister():
    bpy.utils.unregister_class(ShadeSmooth)
    bpy.utils.unregister_class(extorc_pie)
    bpy.utils.unregister_class(pie_operator)
    bpy.utils.unregister_class(SubSurfOp)
    bpy.utils.unregister_class(BoolOp)
    bpy.utils.unregister_class(MirrorOp)
    remove_key_map()

if __name__ == "__main__":
    register()
    