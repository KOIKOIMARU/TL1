import os

import bpy


PROTOTYPE_OBJECT_NAME = "PrototypePlayerSpawn"
PLAYER_SPAWN_OBJECT_NAME = "PlayerSpawn"
PLAYER_SPAWN_TYPE = "PlayerSpawn"


class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    """SpawnPointの複製元モデルを一度だけ読み込む。"""

    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description = "出現ポイントのシンボルをImportします"

    prototype_object_name = PROTOTYPE_OBJECT_NAME
    object_name = PLAYER_SPAWN_OBJECT_NAME

    def execute(self, context):
        if bpy.data.objects.get(self.prototype_object_name) is not None:
            return {"CANCELLED"}

        addon_directory = os.path.dirname(__file__)
        full_path = os.path.join(addon_directory, "player", "player.obj")
        if not os.path.isfile(full_path):
            self.report({"ERROR"}, "SpawnPointモデルが見つかりません")
            return {"CANCELLED"}

        before_objects = set(bpy.data.objects)
        bpy.ops.wm.obj_import(
            "EXEC_DEFAULT",
            filepath=full_path,
            display_type="THUMBNAIL",
            forward_axis="Z",
            up_axis="Y",
        )

        imported_objects = [
            obj for obj in bpy.data.objects if obj not in before_objects
        ]
        if not imported_objects:
            self.report({"ERROR"}, "SpawnPointモデルを読み込めませんでした")
            return {"CANCELLED"}

        prototype = context.active_object or imported_objects[0]
        bpy.ops.object.transform_apply(
            location=False,
            rotation=True,
            scale=False,
            properties=False,
            isolate_users=False,
        )

        prototype.name = self.prototype_object_name
        prototype["type"] = PLAYER_SPAWN_TYPE

        # データは残し、通常のシーン出力には混ざらないよう非表示にする。
        for collection in list(prototype.users_collection):
            collection.objects.unlink(prototype)

        return {"FINISHED"}


class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    """読込済みモデルを共有してSpawnPointをシーンへ配置する。"""

    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    object_name = PLAYER_SPAWN_OBJECT_NAME

    def execute(self, context):
        spawn_object = bpy.data.objects.get(PROTOTYPE_OBJECT_NAME)
        if spawn_object is None:
            result = bpy.ops.myaddon.myaddon_ot_spawn_import_symbol(
                "EXEC_DEFAULT"
            )
            if "FINISHED" not in result:
                self.report({"ERROR"}, "SpawnPointモデルを準備できませんでした")
                return {"CANCELLED"}
            spawn_object = bpy.data.objects.get(PROTOTYPE_OBJECT_NAME)

        if spawn_object is None:
            self.report({"ERROR"}, "SpawnPointモデルが見つかりません")
            return {"CANCELLED"}

        bpy.ops.object.select_all(action="DESELECT")

        created_object = spawn_object.copy()
        context.collection.objects.link(created_object)
        created_object.name = self.object_name
        created_object["type"] = PLAYER_SPAWN_TYPE
        created_object.select_set(True)
        context.view_layer.objects.active = created_object

        return {"FINISHED"}
