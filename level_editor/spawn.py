import os

import bpy


class SpawnNames:
    """出現ポイントの種類ごとに異なる名前とモデルをまとめる。"""

    PROTOTYPE = 0
    INSTANCE = 1
    FILENAME = 2

    names = {
        "Enemy": (
            "PrototypeEnemySpawn",
            "EnemySpawn",
            "needle/needle.obj",
        ),
        "Player": (
            "PrototypePlayerSpawn",
            "PlayerSpawn",
            "player/player.obj",
        ),
    }


class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    """出現ポイント用モデルを初回だけ読み込む。"""

    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description = "出現ポイントのシンボルをImportします"

    def load_obj(self, spawn_type):
        if spawn_type not in SpawnNames.names:
            self.report({'ERROR'}, f"未対応の出現ポイント種類です: {spawn_type}")
            return False

        prototype_name, instance_name, file_name = SpawnNames.names[spawn_type]
        if bpy.data.objects.get(prototype_name) is not None:
            return True

        full_path = os.path.join(os.path.dirname(__file__), file_name)
        if not os.path.isfile(full_path):
            self.report({'ERROR'}, f"モデルファイルが見つかりません: {full_path}")
            return False

        before_objects = set(bpy.data.objects)
        result = bpy.ops.wm.obj_import(
            'EXEC_DEFAULT',
            filepath=full_path,
            display_type='THUMBNAIL',
            forward_axis='Z',
            up_axis='Y',
        )
        if 'FINISHED' not in result:
            self.report({'ERROR'}, f"モデルの読み込みに失敗しました: {file_name}")
            return False

        imported_objects = [obj for obj in bpy.data.objects if obj not in before_objects]
        if not imported_objects:
            self.report({'ERROR'}, f"読み込まれたオブジェクトがありません: {file_name}")
            return False

        prototype = bpy.context.active_object or imported_objects[0]
        bpy.context.view_layer.objects.active = prototype
        prototype.select_set(True)
        bpy.ops.object.transform_apply(
            location=False,
            rotation=True,
            scale=False,
            properties=False,
            isolate_users=False,
        )

        prototype.name = prototype_name
        prototype["type"] = instance_name
        prototype["file_name"] = file_name

        # データベースには残し、シーンから外して複製元としてだけ保持する。
        for collection in list(prototype.users_collection):
            collection.objects.unlink(prototype)
        return True

    def execute(self, context):
        for spawn_type in SpawnNames.names:
            if not self.load_obj(spawn_type):
                return {'CANCELLED'}
        return {'FINISHED'}


class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    """指定種類の出現ポイントを作成して現在のシーンへ配置する。"""

    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty(name="Type", default="Player")

    def execute(self, context):
        if self.type not in SpawnNames.names:
            self.report({'ERROR'}, f"未対応の出現ポイント種類です: {self.type}")
            return {'CANCELLED'}

        prototype_name, instance_name, file_name = SpawnNames.names[self.type]
        spawn_object = bpy.data.objects.get(prototype_name)
        if spawn_object is None:
            result = bpy.ops.myaddon.myaddon_ot_spawn_import_symbol('EXEC_DEFAULT')
            if 'FINISHED' not in result:
                return {'CANCELLED'}
            spawn_object = bpy.data.objects.get(prototype_name)

        if spawn_object is None:
            self.report({'ERROR'}, f"複製元を用意できませんでした: {prototype_name}")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        obj = spawn_object.copy()
        bpy.context.collection.objects.link(obj)
        obj.name = instance_name
        obj["type"] = instance_name
        obj["file_name"] = file_name
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        return {'FINISHED'}


class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    """プレイヤー出現ポイントを作成する。"""

    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤー出現ポイントシンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return bpy.ops.myaddon.myaddon_ot_spawn_create_symbol(
            'EXEC_DEFAULT', type="Player"
        )


class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    """敵出現ポイントを作成する。"""

    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return bpy.ops.myaddon.myaddon_ot_spawn_create_symbol(
            'EXEC_DEFAULT', type="Enemy"
        )
