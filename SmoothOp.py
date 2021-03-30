bl_info = {
    "name": "Extorc Tools",
    "blender": (2, 92, 0),
    "category": "Object",
}

import bpy
from bpy.types import Menu, Operator, Panel
addon_keymaps = []

def getContext(context):
    target = bpy.context.active_object
    lis = bpy.context.selected_objects
    return target, lis

def dup():
    scene=bpy.context.scene
    active = bpy.context.active_object
    data = active.data
    new = bpy.data.objects.new(name = active.name, object_data = data)
    bpy.context.collection.objects.link(new)
    return new

class OriginOp_Geo(Operator):
    """Quick Origin Transfer to Geometry"""
    bl_idname = "extorctools.originop_geo" 
    bl_label = "OriginOp Geo"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        return {'FINISHED'}

class OriginOp_Cur(Operator):
    """Quick Origin Transfer to Geometry"""
    bl_idname = "extorctools.originop_cur" 
    bl_label = "OriginOp Cursor"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}
    
class OriginOp_COS(Operator):
    """Quick Origin Transfer to Geometry"""
    bl_idname = "extorctools.originop_cos" 
    bl_label = "OriginOp Surface"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
       bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
       return {'FINISHED'}
    
class OriginOp_COV(Operator):
    """Quick Origin Transfer to Geometry"""
    bl_idname = "extorctools.originop_cov" 
    bl_label = "OriginOp Volume"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
        return {'FINISHED'}
    
class MirrorOp(Operator):
    """Quick Mirror Operation"""
    bl_idname = "extorctools.mirrorop" 
    bl_label = "Mirror Op"    
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        cutter = []
        target  , lis = getContext(context)
        for x in range(len(lis)):
            if len(lis) == 1:
                raise Exception("2 Objects must be selected")
            elif not lis[x] == target:
                cutter.append(lis[x])
                break
        new_mod = target.modifiers.new(name = f"mir" , type = 'MIRROR')
        new_mod.mirror_object = cutter[0]
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
    
class bool_pie(Menu):
    bl_label = "Bool Tools"
    bl_idname = "extorctoolspie_bool"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("btool.boolean_inters", text = "Intersect Op")
        pie = layout.menu_pie()
        pie.operator("btool.boolean_union", text = "Union Op")
        pie = layout.menu_pie()
        pie.operator("btool.boolean_diff", text = "Difference Op")
        pie = layout.menu_pie()
        pie.operator("btool.boolean_slice", text = "Slice Op")
        
        
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
        pie.operator("extorctools.mirrorop")
        pie = layout.menu_pie()
        pie.operator("org.extorctools_bool")
        pie = layout.menu_pie()
        col2 = pie.column()
        col2.operator("extorctools.originop_geo")
        col2.operator("extorctools.originop_cur")
        col2.operator("extorctools.originop_cos")
        col2.operator("extorctools.originop_cov")
        col = pie.column()

class pie_operator(Operator):
    bl_label = "Pie Caller"
    bl_idname = "org.extorctools" 
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="extorctoolspie")
        return {'FINISHED'}
    
class bool_operator(Operator):
    """Boolean Tools Menu"""
    bl_label = "Bool Op"
    bl_idname = "org.extorctools_bool" 
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="extorctoolspie_bool")
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
    bpy.utils.register_class(MirrorOp)
    bpy.utils.register_class(OriginOp_Geo)
    bpy.utils.register_class(OriginOp_Cur)
    bpy.utils.register_class(OriginOp_COS)
    bpy.utils.register_class(OriginOp_COV)
    bpy.utils.register_class(bool_operator)
    bpy.utils.register_class(bool_pie)
    key_map(pie_operator)
    
def unregister():
    bpy.utils.unregister_class(ShadeSmooth)
    bpy.utils.unregister_class(extorc_pie)
    bpy.utils.unregister_class(pie_operator)
    bpy.utils.unregister_class(SubSurfOp)
    bpy.utils.unregister_class(MirrorOp)
    bpy.utils.unregister_class(OriginOp_Geo)
    bpy.utils.unregister_class(OriginOp_Cur)
    bpy.utils.unregister_class(OriginOp_COS)
    bpy.utils.unregister_class(OriginOp_COV)
    bpy.utils.unregister_class(bool_operator)
    bpy.utils.unregister_class(bool_pie)
    remove_key_map()

if __name__ == "__main__":
    register()