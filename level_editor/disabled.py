import bpy


class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_disabled"
    bl_label = "Add Disabled"
    bl_description = "無効フラグを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object["disabled"] = True
        return {"FINISHED"}


class OBJECT_PT_disabled(bpy.types.Panel):
    bl_idname = "OBJECT_PT_disabled"
    bl_label = "Disabled"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        if "disabled" in context.object:
            self.layout.prop(
                context.object,
                '["disabled"]',
                text="disabled",
            )
        else:
            self.layout.operator(MYADDON_OT_add_disabled.bl_idname)
