import json
import math

import bpy
import bpy_extras


class MYADDON_OT_export_scene(
    bpy.types.Operator,
    bpy_extras.io_utils.ExportHelper,
):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".json"

    def write_and_print(self, file, text):
        print(text)
        file.write(text)
        file.write("\n")

    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始... %r" % self.filepath)

        with open(self.filepath, "wt") as file:
            for obj in bpy.context.scene.objects:
                if obj.parent:
                    continue

                self.parse_scene_recursive(file, obj, 0)

    def parse_scene_recursive(self, file, obj, level):
        """シーン解析用再帰関数"""

        indent = "\t" * level

        self.write_and_print(file, indent + obj.type)

        trans, rot, scale = obj.matrix_local.decompose()
        rot = rot.to_euler()

        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        self.write_and_print(
            file,
            indent + "T %f %f %f" % (trans.x, trans.y, trans.z),
        )
        self.write_and_print(
            file,
            indent + "R %f %f %f" % (rot.x, rot.y, rot.z),
        )
        self.write_and_print(
            file,
            indent + "S %f %f %f" % (scale.x, scale.y, scale.z),
        )

        if "file_name" in obj:
            self.write_and_print(file, indent + "N %s" % obj["file_name"])

        if "collider" in obj:
            self.write_and_print(file, indent + "C %s" % obj["collider"])
            self.write_and_print(
                file,
                indent + "CC %f %f %f" % (
                    obj["collider_center"][0],
                    obj["collider_center"][1],
                    obj["collider_center"][2],
                ),
            )
            self.write_and_print(
                file,
                indent + "CS %f %f %f" % (
                    obj["collider_size"][0],
                    obj["collider_size"][1],
                    obj["collider_size"][2],
                ),
            )

        self.write_and_print(file, indent + "END")
        self.write_and_print(file, "")

        for child in obj.children:
            self.parse_scene_recursive(file, child, level + 1)

    def execute(self, context):
        print("シーン情報をExportします")

        self.export_json()

        self.report({"INFO"}, "シーン情報をExportしました")
        print("シーン情報をExportしました")

        return {"FINISHED"}

    def export_json(self):
        """JSON形式でファイルに出力"""

        json_object_root = {
            "name": "scene",
            "objects": [],
        }

        for obj in bpy.context.scene.objects:
            if obj.parent:
                continue

            self.parse_scene_recursive_json(
                json_object_root["objects"],
                obj,
                0,
            )

        json_text = json.dumps(
            json_object_root,
            ensure_ascii=False,
            cls=json.JSONEncoder,
            indent=4,
        )

        print(json_text)

        with open(self.filepath, "wt", encoding="utf-8") as file:
            file.write(json_text)

    def parse_scene_recursive_json(self, data_parent, obj, level):
        """JSON用の再帰関数"""

        json_object = {
            "type": obj.type,
            "name": obj.name,
        }

        trans, rot, scale = obj.matrix_local.decompose()
        rot = rot.to_euler()

        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        json_object["transform"] = {
            "translation": (trans.x, trans.y, trans.z),
            "rotation": (rot.x, rot.y, rot.z),
            "scaling": (scale.x, scale.y, scale.z),
        }

        if "disabled" in obj:
            json_object["disabled"] = bool(obj["disabled"])

        if "file_name" in obj:
            json_object["file_name"] = obj["file_name"]

        if "collider" in obj:
            json_object["collider"] = {
                "type": obj["collider"],
                "center": obj["collider_center"].to_list(),
                "size": obj["collider_size"].to_list(),
            }

        data_parent.append(json_object)

        if len(obj.children) > 0:
            json_object["children"] = []

            for child in obj.children:
                self.parse_scene_recursive_json(
                    json_object["children"],
                    child,
                    level + 1,
                )
