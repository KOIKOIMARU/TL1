import bpy
import math
import bpy_extras

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Taro Kamata",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# オペレータ：頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました。")
        return {'FINISHED'}


# オペレータ：ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました。")
        return {'FINISHED'}


# オペレータ：シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    bl_options = {'REGISTER', 'UNDO'}

    # 出力するファイルの拡張子
    filename_ext = ".scene"

    # コンソールとファイルに同時出力
    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write("\n")

    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始... %r" % self.filepath)

        # ファイルをテキスト形式で書き出し用にオープン
        with open(self.filepath, "wt") as file:

            # シーン内の全オブジェクトについて
            for object in bpy.context.scene.objects:

                # 親オブジェクトがあるものはスキップ
                if object.parent:
                    continue

                # ルート直下のオブジェクトを起点に再帰処理
                self.parse_scene_recursive(file, object, 0)

    def parse_scene_recursive(self, file, object, level):
        """シーン解析用再帰関数"""

        # 深さ分インデントする
        indent = ""
        for i in range(level):
            indent += "\t"

        # オブジェクト種類を書き込み
        self.write_and_print(file, indent + object.type)

        # ローカルトランスフォーム行列から移動、回転、スケーリングを取得
        trans, rot, scale = object.matrix_local.decompose()

        # 回転をQuaternionからEuler角に変換
        rot = rot.to_euler()

        # ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        # トランスフォーム情報を書き込み
        self.write_and_print(
            file,
            indent + "T %f %f %f" % (trans.x, trans.y, trans.z)
        )
        self.write_and_print(
            file,
            indent + "R %f %f %f" % (rot.x, rot.y, rot.z)
        )
        self.write_and_print(
            file,
            indent + "S %f %f %f" % (scale.x, scale.y, scale.z)
        )

        # カスタムプロパティ file_name があれば書き込み
        if "file_name" in object:
            self.write_and_print(
                file,
                indent + "N %s" % object["file_name"]
            )

        self.write_and_print(file, indent + "END")
        self.write_and_print(file, "")

        # 子オブジェクトへ進む
        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)

    def execute(self, context):
        print("シーン情報をExportします")

        # ファイルに出力
        self.export()

        self.report({'INFO'}, "シーン情報をExportしました")
        print("シーン情報をExportしました")

        return {'FINISHED'}


# オペレータ：カスタムプロパティ「file_name」追加
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName 追加"
    bl_description = "file_name カスタムプロパティを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object["file_name"] = ""
        return {'FINISHED'}


# パネル：ファイル名
class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""

    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"

    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        # file_name があればプロパティを表示
        if "file_name" in context.object:
            self.layout.prop(context.object, '["file_name"]', text=self.bl_label)

        # なければ追加ボタンを表示
        else:
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)


# サブメニュークラス
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):
        self.layout.operator(
            MYADDON_OT_stretch_vertex.bl_idname,
            text=MYADDON_OT_stretch_vertex.bl_label
        )

        self.layout.operator(
            MYADDON_OT_create_ico_sphere.bl_idname,
            text=MYADDON_OT_create_ico_sphere.bl_label
        )

        self.layout.operator(
            MYADDON_OT_export_scene.bl_idname,
            text=MYADDON_OT_export_scene.bl_label
        )

    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    MYADDON_OT_add_filename,
    TOPBAR_MT_my_menu,
    OBJECT_PT_file_name,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました。")


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました。")


if __name__ == "__main__":
    register()