import umaModelReplace
import shutil

uma = umaModelReplace.UmaReplace()


def getAndReplaceTexture2D(bundle_hash, src_names):
    is_not_exist, msg = uma.get_texture_in_bundle(bundle_hash, src_names)
    if not is_not_exist:
        print(f"Unpacked resources already exist: {msg}")
        do_replace = input('Enter "Y" to overwrite unpacked resources, or enter anything else to skip export: ')
        if do_replace in ["Y", "y"]:
            _, msg = uma.get_texture_in_bundle(bundle_hash, src_names, True)

    print(f"Resource export attempted. Please check the directory: {msg}")
    do_fin = input(
        'Please modify/replace the files. When finished, enter "Y" to repackage and replace the game files.\n'
        'If you don’t want to modify now, enter anything else to exit. Next time you can choose "skip export".\n'
        "Input: "
    )
    if do_fin.strip() in ["Y", "y"]:
        uma.file_backup(bundle_hash)
        edited_path = uma.replace_texture2d(bundle_hash)
        shutil.copyfile(edited_path, uma.get_bundle_path(bundle_hash))
        print("Texture has been modified")


# Example usage:
# getAndReplaceTexture2D("EUI2AY3HRHIRXFCU5ZUTQRQKS4IJGBF5", ["tex_env_cutin1019_40_00_base01"])  # Digimon Unique Skill "Reverence"
# getAndReplaceTexture2D("L6XWAMB2FBPJK32AEWJUMUDB47BJQROC", ["tex_chr_prop1259_00_diff"])  # Digimon Unique Skill - Doll
getAndReplaceTexture2D("KM6Z67WZ5C6XUQZBLXJ237TBVVVAGFCS", ["tex_chr_prop1003_06_diff"])  # Magazine Cover
