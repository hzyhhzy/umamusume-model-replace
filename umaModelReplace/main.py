import UnityPy
import sqlite3
import os
import shutil
import typing as t
from PIL import Image

if __name__ == '__main__':
    import assets_path
else:
    from . import assets_path

spath = os.path.split(__file__)[0]
BACKUP_PATH = f"{spath}/backup"
EDITED_PATH = f"{spath}/edited"


class UmaFileNotFoundError(FileNotFoundError):
    pass

def replace_raw1(data: bytes, old: bytes, new: bytes, context: int = 20) -> bytes:
    """
    在 data 中将所有 old 替换为 new，并在每次替换时打印上下文。
    
    :param data: 原始字节串
    :param old: 需要被替换的字节串
    :param new: 替换成的字节串
    :param context: 打印时，替换位置前后各保留多少字节上下文
    :return: 完成所有替换后的新字节串
    """

    any_replaced=False
    result = bytearray()
    i = 0
    while True:
        idx = data.find(old, i)
        if idx < 0:
            # 无更多匹配，添加剩余部分
            result.extend(data[i:])
            break
        any_replaced=True
        # 计算上下文的起止位置
        start = max(idx - context, 0)
        end = min(idx + len(old) + context, len(data))

        before = data[start:idx]
        match = data[idx:idx + len(old)]
        after = data[idx + len(old):end]
        match2 = data[max(0,idx-30):min(idx + len(old)+30,len(data))]



        # 打印信息
        #print(f"Match at byte offset {idx}:")
        #print(f"  …{before!r}[{match!r}]{after!r}…")
        print(f"{match2}")


        # 构造结果
        result.extend(data[i:idx])
        result.extend(new)
        i = idx + len(old)
    if(any_replaced):
        print("replaced")


    #result=result.replace("chr1024_00/textures/tex_chr1024_00_cheek0".encode("utf8"), "chr9002_00/textures/tex_chr9002_00_cheek0".encode("utf8"))
    return bytes(result),any_replaced

def replace_raw(data: bytes, old:  bytes, new:  bytes, context: int = 20, cab_mapping: dict = None) -> tuple[bytes, bool]:
    """
    在 data 中匹配特定模式并替换ID，只替换指定的模式，其他地方不变。
    
    :param data: 原始字节串
    :param old: 原始ID字节串，例如 b"9002_00"
    :param new: 新ID字节串，例如 b"1024_00"
    :param context: 打印时，替换位置前后各保留多少字节上下文
    :param cab_mapping: CAB序号映射字典，格式为 {orig_cab: new_cab}
    :return: (完成所有替换后的新字节串, 是否有替换发生)
    """
    import re
    
    any_replaced = False
    result = data
    
    # 定义需要匹配的模式列表
    patterns = [
        # 模式1: \x00pfb_bdy{id}\x00
        b'\x00pfb_bdy' + old + b'\x00',
        # 模式2: /bdy{id}/pfb_bdy{id}
        b'/bdy' + old + b'/pfb_bdy' + old,
        # 未来可以在这里添加更多模式
        b'/chr' + old + b'/pfb_chr' + old,
        b'\x00tex_chr' + old + b'_cheek1\x00',
        b'\x00ast_chr' + old + b'_ear_target\x00',
        b'\x00ast_chr' + old + b'_facial_target',
        b'\x00pfb_chr' + old + b'\x00',
        b'\x00mtl_chr' + old,
    ]
    
    # 对应的替换模式
    replacements = [
        # 替换1: \x00pfb_bdy{new_id}\x00
        b'\x00pfb_bdy' + new + b'\x00',
        # 替换2: /bdy{new_id}/pfb_bdy{new_id}
        b'/bdy' + new + b'/pfb_bdy' + new,
        # 替换3: \x00tex_chr{new_id}_cheek1\x00
        b'/chr' + new + b'/pfb_chr' + new,
        b'\x00tex_chr' + new + b'_cheek1\x00',
        b'\x00ast_chr' + new + b'_ear_target\x00',
        b'\x00ast_chr' + new + b'_facial_target',
        b'\x00pfb_chr' + new + b'\x00',
        b'\x00mtl_chr' + new,

    ]
    
    # 逐个处理每个模式
    for pattern, replacement in zip(patterns, replacements):
        #print(pattern,replacement)
        if pattern in result:
            # 找到所有匹配位置用于调试输出
            matches = []
            start = 0
            while True:
                idx = result.find(pattern, start)
                if idx == -1:
                    break
                matches.append(idx)
                start = idx + 1
            
            if matches:
                any_replaced = True
                # 输出调试信息
                for idx in matches:
                    start_ctx = max(0, idx - context)
                    end_ctx = min(len(result), idx + len(pattern) + context)
                    match_context = result[start_ctx:end_ctx]
                    #print(f"Pattern match at offset {idx}: {match_context}")
                
                # 执行替换
                result = result.replace(pattern, replacement)
                #print(f"Replaced pattern: {pattern} -> {replacement}")
    
    # 如果提供了CAB映射，则进行CAB序号替换
    if cab_mapping:
        for orig_cab, new_cab in cab_mapping.items():
            orig_cab_bytes = orig_cab.encode('utf-8')
            new_cab_bytes = new_cab.encode('utf-8')
            if orig_cab_bytes in result:
                result = result.replace(orig_cab_bytes, new_cab_bytes)
                any_replaced = True
                #print(f"CAB替换: {orig_cab} -> {new_cab}")
    
    return result, any_replaced

class UmaReplace:
    def __init__(self):
        self.init_folders()
        profile_path = os.environ.get("UserProfile")
        self.base_path = f"{profile_path}/AppData/LocalLow/Cygames/umamusume"
        self.conn = sqlite3.connect(f"{self.base_path}/meta")
        self.master_conn = sqlite3.connect(f"{self.base_path}/master/master.mdb")

    @staticmethod
    def init_folders():
        if not os.path.isdir(BACKUP_PATH):
            os.makedirs(BACKUP_PATH)
        if not os.path.isdir(EDITED_PATH):
            os.makedirs(EDITED_PATH)

    def get_bundle_path(self, bundle_hash: str):
        return f"{self.base_path}/dat/{bundle_hash[:2]}/{bundle_hash}"

    def file_backup(self, bundle_hash: str):
        if not os.path.isfile(f"{BACKUP_PATH}/{bundle_hash}"):
            shutil.copyfile(f"{self.get_bundle_path(bundle_hash)}", f"{BACKUP_PATH}/{bundle_hash}")

    def file_restore(self, hashs: t.Optional[t.List[str]] = None):
        """
        恢复备份
        :param hashs: bundle hash 列表, 若为 None, 则恢复备份文件夹内所有文件
        """
        if not hashs:
            hashs = os.listdir(BACKUP_PATH)
        if not isinstance(hashs, list):
            raise TypeError(f"hashs must be a list, not {type(hashs)}")

        for i in hashs:
            fpath = f"{BACKUP_PATH}/{i}"
            if os.path.isfile(fpath):
                shutil.copyfile(fpath, self.get_bundle_path(i))
                print(f"restore {i}")


    def get_cab_mapping(self, orig_paths: list, new_paths: list, id_orig: str = None, id_new: str = None) -> dict:
        """
        获取orig_paths与new_paths的cab序号映射
        
        :param orig_paths: 原始逻辑路径列表
        :param new_paths: 新逻辑路径列表
        :param id_orig: 原始ID，用于hash查找
        :param id_new: 新ID，用于hash查找
        :return: {orig_cab: new_cab} 的映射字典
        """
        mapping = {}
        
        for orig_path, new_path in zip(orig_paths, new_paths):
            try:
                # 将逻辑路径转换为实际文件路径
                orig_hash = self.get_bundle_hash(orig_path, id_orig)
                new_hash = self.get_bundle_hash(new_path, id_new)
                orig_file_path = self.get_bundle_path(orig_hash)
                new_file_path = self.get_bundle_path(new_hash)
                
                # 加载原始文件获取cab序号
                orig_env = UnityPy.load(orig_file_path)
                orig_cabs = list(orig_env.cabs.keys())
                
                # 加载新文件获取cab序号
                new_env = UnityPy.load(new_file_path)
                new_cabs = list(new_env.cabs.keys())
            except Exception as e:
                print(f"跳过文件 {orig_path} -> {new_path}: {e}")
                continue
            
            # 断言验证cab序号的数量和格式
            assert len(orig_cabs) in [1, 2], f"原始文件 {orig_path} 的cab数量应该是1或2，实际是 {len(orig_cabs)}"
            assert len(new_cabs) in [1, 2], f"新文件 {new_path} 的cab数量应该是1或2，实际是 {len(new_cabs)}"
            
            # 获取较短的cab序号（不带.ress后缀的）
            def get_main_cab(cabs):
                if len(cabs) == 1:
                    cab = cabs[0]
                else:
                    # 找到较短的那个（不带.ress后缀）
                    shorter = min(cabs, key=len)
                    longer = max(cabs, key=len)
                    assert longer == shorter + ".ress", f"两个cab序号应该是主序号和主序号+.ress的关系，实际是 {shorter} 和 {longer}"
                    cab = shorter
                
                # 去掉"cab-"前缀
                if cab.startswith("cab-"):
                    return cab[4:]  # 去掉"cab-"前缀
                else:
                    assert False
                return cab
            
            orig_main_cab = get_main_cab(orig_cabs)
            new_main_cab = get_main_cab(new_cabs)
            
            #mapping[orig_main_cab] = new_main_cab
            #print(f"路径 {orig_path} -> {new_path}: CAB映射 {orig_main_cab} -> {new_main_cab}")
            mapping[new_main_cab] = orig_main_cab
            print(f"CAB映射 {new_main_cab} -> {orig_main_cab}")
        
        return mapping

    @staticmethod
    def replace_file_path(fname: str, id1: str, id2: str, save_name: t.Optional[str] = None, cab_mapping: dict = None) -> str:
        # 获取CAB序号
        env = UnityPy.load(fname)
        #print(f"CAB序号: {env.cabs.keys()}")
        
        # CAB替换将在文件保存时统一处理
        
        #print(fname)
        data = None

        for obj in env.objects:
            #if obj.type.name not in ["Avatar"]:
            data = obj.read()
            # print(obj.type.name, data.name)
            if obj.type.name == "MonoBehaviour":
                if(hasattr(data,"raw_data")):
                    raw = bytes(data.raw_data)
                    raw,changed = replace_raw(raw, old=id1.encode("utf8"), new=id2.encode("utf8"), cab_mapping=cab_mapping)

                    data.set_raw_data(raw)
                    data.save(raw_data=raw)
                    #if(changed):
                    #    print(data.m_Name)
                else:
                    raw = bytes(obj.get_raw_data())
                    raw,changed = replace_raw(raw, old=id1.encode("utf8"), new=id2.encode("utf8"), cab_mapping=cab_mapping)

                    obj.set_raw_data(raw)
                    #if(changed):
                    #    print(data.m_Name)
                
            else:
                #print(obj.type.name)
                raw = bytes(obj.get_raw_data())
                raw,changed = replace_raw(raw, old=id1.encode("utf8"), new=id2.encode("utf8"), cab_mapping=cab_mapping)
                obj.set_raw_data(raw)
                #if(changed):
                #    print(data.m_Name)
                #obj.save()
        
        if save_name is None:
            save_name = f"{EDITED_PATH}/{os.path.split(fname)[-1]}"
        if data is None:
            with open(fname, "rb") as f:
                data = f.read()
                data,changed = replace_raw(data, old=id1.encode("utf8"), new=id2.encode("utf8"), cab_mapping=cab_mapping)

            with open(save_name, "wb") as f:
                f.write(data)
        else:
            with open(save_name, "wb") as f:
                file_data = env.file.save()
                # 如果提供了CAB映射，则在文件数据中进行CAB替换
                if cab_mapping:
                    for orig_cab, new_cab in cab_mapping.items():
                        orig_cab_bytes = orig_cab.encode('utf-8')
                        new_cab_bytes = new_cab.encode('utf-8')
                        if orig_cab_bytes in file_data:
                            file_data = file_data.replace(orig_cab_bytes, new_cab_bytes)
                            #print(f"文件级CAB替换: {orig_cab} -> {new_cab}")
                f.write(file_data)
        return save_name

    def replace_texture2d(self, bundle_name: str):
        edited_path = f"./editTexture/{bundle_name}"
        if not os.path.isdir(edited_path):
            raise UmaFileNotFoundError(f"path: {edited_path} not found. Please extract first.")

        file_names = os.listdir(edited_path)

        env = UnityPy.load(self.get_bundle_path(bundle_name))
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if hasattr(data, "m_Name"):
                    if f"{data.m_Name}.png" in file_names:
                        data.image = Image.open(f"{edited_path}/{data.m_Name}.png")
                        data.save()

        save_name = f"{EDITED_PATH}/{os.path.split(bundle_name)[-1]}"
        with open(save_name, "wb") as f:
            f.write(env.file.save())
        return save_name

    def get_texture_in_bundle(self, bundle_name: str, src_names: t.Optional[t.List[str]], force_replace=False):
        base_path = f"./editTexture/{bundle_name}"
        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        if not force_replace:
            if len(os.listdir(base_path)) > 0:
                return False, base_path

        env = UnityPy.load(self.get_bundle_path(bundle_name))
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if hasattr(data, "m_Name"):
                    if src_names is None or (data.m_Name in src_names):
                        #img_data = data.get_image_data()
                        #image: Image = img_data.image
                        image = data.image
                        image.save(f"{base_path}/{data.m_Name}.png")
                        print(f"save {data.m_Name} into {f'{base_path}/{data.m_Name}.png'}")
        return True, base_path

    def get_bundle_hash(self, path: str, query_orig_id: t.Optional[str]) -> str:
        cursor = self.conn.cursor()
        query = cursor.execute("SELECT h FROM a WHERE n=?", [path]).fetchone()
        if query is None:
            if (query_orig_id is not None) and ("_" in query_orig_id):
                query_id, query_sub_id = query_orig_id.split("_")

                if query is None:
                    new_path = path.replace(query_orig_id, f"{query_id}_%")
                    query = cursor.execute("SELECT h, n FROM a WHERE n LIKE ?", [new_path]).fetchone()
                    if query is not None:
                        print(f"{path} not found, but found {query[1]}")

        if query is None:
            raise UmaFileNotFoundError(f"{path} not found!")

        cursor.close()
        return query[0]

    def save_char_body_texture(self, char_id: str, force_replace=False):
        mtl_bdy_path = assets_path.get_body_mtl_path(char_id)
        bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
        return self.get_texture_in_bundle(bundle_hash, assets_path.get_body_mtl_names(char_id), force_replace)

    def save_char_head_texture(self, char_id: str, force_replace=False, on_index=-1):
        ret = []
        for n, i in enumerate(assets_path.get_head_mtl_path(char_id)):
            if on_index != -1:
                if n != on_index:
                    continue
            bundle_hash = self.get_bundle_hash(i, None)
            ret.append(self.get_texture_in_bundle(bundle_hash, None, force_replace))
        return ret

    def replace_char_body_texture(self, char_id: str):
        mtl_bdy_path = assets_path.get_body_mtl_path(char_id)
        print(mtl_bdy_path)
        bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
        self.file_backup(bundle_hash)
        edited_path = self.replace_texture2d(bundle_hash)
        # print("save", edited_path)
        shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))

    def replace_char_head_texture(self, char_id: str):
        for mtl_bdy_path in assets_path.get_head_mtl_path(char_id):
            bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
            self.file_backup(bundle_hash)
            edited_path = self.replace_texture2d(bundle_hash)
            # print("save", edited_path)
            shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))

    def replace_file_ids(self, orig_path: str, new_path: str, id_orig: str, id_new: str, cab_mapping: dict = None):
        orig_hash = self.get_bundle_hash(orig_path, id_orig)
        new_hash = self.get_bundle_hash(new_path, id_new)
        self.file_backup(orig_hash)
        edt_bundle_file_path = self.replace_file_path(self.get_bundle_path(new_hash), id_new, id_orig,
                                                      f"{EDITED_PATH}/{orig_hash}", cab_mapping=cab_mapping)
        shutil.copyfile(edt_bundle_file_path, self.get_bundle_path(orig_hash))

    def replace_body(self, id_orig: str, id_new: str):
        """
        替换身体
        :param id_orig: 原id, 例: 1046_01
        :param id_new: 新id
        """
        orig_paths = assets_path.get_body_path(id_orig)
        new_paths = assets_path.get_body_path(id_new)
        
        # 获取CAB序号映射
        try:
            cab_mapping = self.get_cab_mapping(orig_paths, new_paths, id_orig, id_new)
            #print(f"Body替换CAB映射: {cab_mapping}")
        except Exception as e:
            print(f"获取Body CAB映射失败: {e}")
        
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new, cab_mapping)
            except UmaFileNotFoundError as e:
                print(e)

    def replace_head(self, id_orig: str, id_new: str):
        """
        替换头部
        :param id_orig: 原id, 例: 1046_01
        :param id_new: 新id
        """
        orig_paths = assets_path.get_head_path(id_orig)
        new_paths = assets_path.get_head_path(id_new)
        
        # 获取CAB序号映射
        try:
            cab_mapping = self.get_cab_mapping(orig_paths, new_paths, id_orig, id_new)
            #print(f"Head替换CAB映射: {cab_mapping}")
        except Exception as e:
            print(f"获取Head CAB映射失败: {e}")
        
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new, cab_mapping)
            except UmaFileNotFoundError as e:
                print(e)

    def replace_tail(self, id_orig: str, id_new: str):  # 目前无法跨模型更换尾巴, 更换目标不能和原马娘同时出场。
        """
        替换尾巴
        :param id_orig: 原id, 例: 1046
        :param id_new: 新id
        """

        def check_vaild_path(paths: list):
            try:
                self.get_bundle_hash(paths[0], None)
            except UmaFileNotFoundError:
                return False
            return True

        orig_paths1 = assets_path.get_tail1_path(id_orig)
        orig_paths2 = assets_path.get_tail2_path(id_orig)

        new_paths1 = assets_path.get_tail1_path(id_new)
        new_paths2 = assets_path.get_tail2_path(id_new)

        orig_paths = None
        new_paths = None
        use_id1 = -1
        use_id2 = -1
        if check_vaild_path(orig_paths1):
            orig_paths = orig_paths1
            use_id1 = 1
        if check_vaild_path(orig_paths2):
            orig_paths = orig_paths2
            use_id1 = 2
        if check_vaild_path(new_paths1):
            new_paths = new_paths1
            use_id2 = 1
        if check_vaild_path(new_paths2):
            use_id2 = 2
            new_paths = new_paths2

        if (orig_paths is None) or (new_paths is None):
            print("tail not found")
            return

        if use_id1 != use_id2:
            print(f"{id_orig} 模型编号: {use_id1}, {id_new} 模型编号: {use_id2}, 目前无法跨模型修改尾巴。")
            return
        print("注意, 更换尾巴后, 更换目标不能和原马娘同时出场。")
        
        # 获取CAB序号映射
        try:
            cab_mapping = self.get_cab_mapping(orig_paths, new_paths, id_orig, id_new)
            #print(f"Tail替换CAB映射: {cab_mapping}")
        except Exception as e:
            print(f"获取Tail CAB映射失败: {e}")
        
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new, cab_mapping)
            except UmaFileNotFoundError as e:
                print(e)

    def edit_gac_chr_start(self, dress_id: str, type: str):
        """
        替换开门人物
        :param dress_id: 目标开门id, 例: 100101
        :param type: 001骏川手纲，002秋川弥生
        """

        def edit_chr(orig_hash: str, dress_id: str):
            env = UnityPy.load(self.get_bundle_path(orig_hash))
            for obj in env.objects:
                if obj.type.name == "MonoBehaviour":
                    if obj.serialized_type.nodes:
                        tree = obj.read_typetree()
                        if "runtime_gac_chr_start_00" in tree["m_Name"]:
                            tree["_characterList"][0]["_characterKeys"]["_selectCharaId"] = int(dress_id[:-2])
                            tree["_characterList"][0]["_characterKeys"]["_selectClothId"] = int(dress_id)
                            obj.save_typetree(tree)
            with open(f"{EDITED_PATH}/{orig_hash}", "wb") as f:
                f.write(env.file.save())

        path = assets_path.get_gac_chr_start_path(type)
        orig_hash = self.get_bundle_hash(path, None)
        self.file_backup(orig_hash)
        edit_chr(orig_hash, dress_id)
        shutil.copyfile(f"{EDITED_PATH}/{orig_hash}", self.get_bundle_path(orig_hash))

    def edit_cutin_skill(self, id_orig: str, id_target: str):
        """
        替换技能
        :param id_orig: 原id, 例: 100101
        :param id_target: 新id
        """
        target_path = assets_path.get_cutin_skill_path(id_target)
        target_hash = self.get_bundle_hash(target_path, None)
        target = UnityPy.load(self.get_bundle_path(target_hash))

        target_tree = None
        target_clothe_id = None
        target_cy_spring_name_list = None

        for obj in target.objects:
            if obj.type.name == "MonoBehaviour":
                if obj.serialized_type.nodes:
                    tree = obj.read_typetree()
                    if "runtime_crd1" in tree["m_Name"]:
                        target_tree = tree
                        for character in tree["_characterList"]:
                            target_clothe_id = str(character["_characterKeys"]["_selectClothId"])

        if target_tree is None:
            print("目标无法解析")
            return

        for character in target_tree["_characterList"]:
            for targetList in character["_characterKeys"]["thisList"]:
                if len(targetList["_enableCySpringList"]) > 0:
                    target_cy_spring_name_list = targetList["_targetCySpringNameList"]

        orig_path = assets_path.get_cutin_skill_path(id_orig)
        orig_hash = self.get_bundle_hash(orig_path, None)
        self.file_backup(orig_hash)
        env = UnityPy.load(self.get_bundle_path(orig_hash))

        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                if obj.serialized_type.nodes:
                    tree = obj.read_typetree()
                    if "runtime_crd1" in tree["m_Name"]:
                        for character in tree["_characterList"]:
                            character["_characterKeys"]["_selectCharaId"] = int(target_clothe_id[:-2])
                            character["_characterKeys"]["_selectClothId"] = int(target_clothe_id)
                            character["_characterKeys"]["_selectHeadId"] = 0
                            for outputList in character["_characterKeys"]["thisList"]:
                                if len(outputList["_enableCySpringList"]) > 0:
                                    outputList["_enableCySpringList"] = [1] * len(target_cy_spring_name_list)
                                    outputList["_targetCySpringNameList"] = target_cy_spring_name_list
                        obj.save_typetree(tree)

        with open(f"{EDITED_PATH}/{orig_hash}", "wb") as f:
            f.write(env.file.save())
        shutil.copyfile(f"{EDITED_PATH}/{orig_hash}", self.get_bundle_path(orig_hash))
        print("替换完成")

    def replace_race_result(self, id_orig: str, id_new: str):
        """
        替换G1胜利动作
        :param id_orig: 原id, 例: 100101
        :param id_new: 新id
        """
        orig_paths = assets_path.get_crd_race_result_path(id_orig)
        new_paths = assets_path.get_crd_race_result_path(id_new)
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new)
            except UmaFileNotFoundError as e:
                print(e)

    def unlock_live_dress(self):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        def get_all_dress_in_table():
            self.master_conn.row_factory = dict_factory
            cursor = self.master_conn.cursor()
            cursor.execute("SELECT * FROM dress_data")
            # fetchall as result
            query = cursor.fetchall()
            # close connection
            cursor.close()
            return query

        def get_unique_in_table():
            self.conn.row_factory = dict_factory
            cursor = self.conn.cursor()
            cursor.execute("SELECT n FROM a WHERE n like '%pfb_chr1____90'")
            # fetchall as result
            names = cursor.fetchall()
            # close connection
            cursor.close()
            list = []
            for name in names:
                list.append(name["n"][-7:-3])
            return list

        def create_data(dress, unique):
            dress['id'] = dress['id'] + 89
            dress['body_type_sub'] = 90
            if str(dress['id'])[:-2] in set(unique):
                dress['head_sub_id'] = 90
            else:
                dress['head_sub_id'] = 0
            self.master_conn.row_factory = dict_factory
            cursor = self.master_conn.cursor()
            cursor.execute("INSERT INTO dress_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           [dress['id'], dress['condition_type'], dress['have_mini'], dress['general_purpose'],
                            dress['costume_type'], dress['chara_id'], dress['use_gender'], dress['body_shape'],
                            dress['body_type'], dress['body_type_sub'], dress['body_setting'], dress['use_race'],
                            dress['use_live'], dress['use_live_theater'], dress['use_home'], dress['use_dress_change'],
                            dress['is_wet'], dress['is_dirt'], dress['head_sub_id'], dress['use_season'],
                            dress['dress_color_main'], dress['dress_color_sub'], dress['color_num'],
                            dress['disp_order'],
                            dress['tail_model_id'], dress['tail_model_sub_id'], dress['mini_mayu_shader_type'],
                            dress['start_time'], dress['end_time']])
            self.master_conn.commit()
            cursor.close()

        def unlock_data():
            self.master_conn.row_factory = dict_factory
            cursor = self.master_conn.cursor()
            cursor.execute("UPDATE dress_data SET use_live = 1, use_live_theater = 1")
            self.master_conn.commit()
            cursor.close()

        dresses = get_all_dress_in_table()
        unique = get_unique_in_table()
        for dress in dresses:
            if 100000 < dress['id'] < 200000 and str(dress['id']).endswith('01'):
                create_data(dress, unique)
        unlock_data()

    def clear_live_blur(self, edit_id: str):
        cursor = self.conn.cursor()
        query = cursor.execute("SELECT h, n FROM a WHERE n LIKE 'cutt/cutt_son%/son%_camera'").fetchall()
        bundle_names = [i[0] for i in query]
        path_names = [i[1] for i in query]
        cursor.close()
        target_path = f"cutt/cutt_son{edit_id}/son{edit_id}_camera" if edit_id != "" else None
        tLen = len(bundle_names)

        for n, bn in enumerate(bundle_names):
            path_name = path_names[n]
            if target_path is not None:
                if path_name != target_path:
                    continue
            print(f"Editing: {path_name} ({n + 1}/{tLen})")
            try:
                bundle_path = self.get_bundle_path(bn)
                if not os.path.isfile(bundle_path):
                    print(f"File not found: {bundle_path}")
                    continue
                env = UnityPy.load(bundle_path)
                for obj in env.objects:
                    if obj.type.name == "MonoBehaviour":
                        if not obj.serialized_type.nodes:
                            continue
                        tree = obj.read_typetree()

                        tree['postEffectDOFKeys']['thisList'] = [tree['postEffectDOFKeys']['thisList'][0]]
                        dof_set_data = {
                            "frame": 0,
                            "attribute": 327680,
                            "interpolateType": 0,
                            "curve": {
                                "m_Curve": [],
                                "m_PreInfinity": 2,
                                "m_PostInfinity": 2,
                                "m_RotationOrder": 4
                            },
                            "easingType": 0,
                            "forcalSize": 30.0,
                            "blurSpread": 20.0,
                            "charactor": 1,
                            "dofBlurType": 3,
                            "dofQuality": 1,
                            "dofForegroundSize": 0.0,
                            "dofFgBlurSpread": 1.0,
                            "dofFocalPoint": 1.0,
                            "dofSmoothness": 1.0,
                            "BallBlurPowerFactor": 0.0,
                            "BallBlurBrightnessThreshhold": 0.0,
                            "BallBlurBrightnessIntensity": 1.0,
                            "BallBlurSpread": 0.0
                        }
                        for k in dof_set_data:
                            tree['postEffectDOFKeys']['thisList'][0][k] = dof_set_data[k]

                        tree['postEffectBloomDiffusionKeys']['thisList'] = []
                        tree['radialBlurKeys']['thisList'] = []

                        obj.save_typetree(tree)

                self.file_backup(bn)
                with open(bundle_path, 'wb') as f:
                    f.write(env.file.save())

            except Exception as e:
                print(f"Exception occurred when editing file: {bn}\n{e}")

        print("done.")

if __name__ == '__main__':
    # 测试代码，仅在直接运行此文件时执行
    a = UmaReplace()
    a.file_restore()
    for i in range(1001, 1135):
        a.replace_body(f"{i}_00", "9002_00")
        a.replace_head(f"{i}_00", "9002_00")
    pass
