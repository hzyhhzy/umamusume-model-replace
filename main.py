import os
import winreg
import json
import vdf

import umaModelReplace

def get_dmm_game_path() -> str | None:
    profile_path = os.environ.get("UserProfile")
    if profile_path is None:
        return None

    legacy_data_path = os.path.join(profile_path, "AppData",
                                    "LocalLow", "Cygames", "umamusume")
    if os.path.isfile(os.path.join(legacy_data_path, "meta")):
        return legacy_data_path
    else:
        dmm_config_path = os.path.join(profile_path, "AppData", "Roaming",
                                       "dmmgameplayer5", "dmmgame.cnf")
        dmm_config = json.load(open(dmm_config_path, "r", encoding="utf-8"))
        for product in dmm_config["contents"]:
            if product["productId"] == "umamusume":
                game_path = product["detail"]["path"]
                return os.path.join(game_path, "umamusume_Data",
                                    "Persistent")

def get_steam_game_path() -> str | None:
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\Valve\\Steam")
        steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
        winreg.CloseKey(key)
    except FileNotFoundError:
        try:
            # does this game even run on 32 bit windows lul
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Valve\\Steam")
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            winreg.CloseKey(key)
        except FileNotFoundError:
            return None

    libraryfolders_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
    libraryfolders = vdf.load(open(libraryfolders_path, "r", encoding="utf-8"))

    for library in libraryfolders["libraryfolders"].values():
        if "3564400" in library["apps"]:
            steam_path = library["path"]
    game_path = os.path.join(steam_path, "steamapps", "common",
                                "UmamusumePrettyDerby_Jpn",
                                "UmamusumePrettyDerby_Jpn_Data",
                                "Persistent")
    if os.path.isdir(game_path):
        return game_path
    else:
        return None

def replace_char_body_texture(uma: umaModelReplace.UmaReplace, char_id: str):
    is_not_exist, msg = uma.save_char_body_texture(char_id, False)
    if not is_not_exist:
        print(f"Unpacked resources already exist: {msg}")
        do_replace = input('Enter "Y" to overwrite unpacked resources, or enter anything else to skip export: ')
        if do_replace in ["Y", "y"]:
            _, msg = uma.save_char_body_texture(char_id, True)

    print(f"Resource export attempted. Please check the directory: {msg}")
    do_fin = input(
        'Please modify/replace the files. When finished, enter "Y" to repackage and replace the game files.\n'
        'If you don’t want to modify now, enter anything else to exit. Next time you can choose "skip export".\n'
        "Input: "
    )
    if do_fin.strip() in ["Y", "y"]:
        uma.replace_char_body_texture(char_id)
        print("Texture has been modified")


def replace_char_head_texture(uma: umaModelReplace.UmaReplace, char_id: str):
    for n, i in enumerate(uma.save_char_head_texture(char_id, False)):
        is_not_exist, msg = i

        if not is_not_exist:
            print(f"Unpacked resources already exist: {msg}")
            do_replace = input('Enter "Y" to overwrite unpacked resources, or enter anything else to skip export: ')
            if do_replace in ["Y", "y"]:
                _, msg = uma.save_char_head_texture(char_id, True, n)[0]

        print(f"Resource export attempted. Please check the directory: {msg}")

    do_fin = input(
        'Please modify/replace the files. When finished, enter "Y" to repackage and replace the game files.\n'
        'If you don’t want to modify now, enter anything else to exit. Next time you can choose "skip export".\n'
        "Input: "
    )
    if do_fin.strip() in ["Y", "y"]:
        uma.replace_char_head_texture(char_id)
        print("Texture has been modified")


if __name__ == "__main__":
    # this could be way better with list comprehension lol
    available_paths = []
    available_paths += [get_dmm_game_path()] if get_dmm_game_path() is not None else []
    available_paths += [get_steam_game_path()] if get_steam_game_path() is not None else []

    base_path = ""
    if len(available_paths) == 0:
        print("Unable to locate UM:PD game directory\n")
        exit(1)
    elif len(available_paths) == 1:
        base_path = available_paths[0]

    while not base_path:
        print("Multiple game directories detected:\n")
        do_type = input(
            f"[1] DMM - {available_paths[0]}\n"
            f"[2] Steam - {available_paths[1]}\n"
            "[99] Exit\n"
            "Please select an option: "
        )

        if do_type == "1":
            base_path = available_paths[0]
        elif do_type == "2":
            base_path = available_paths[1]
        elif do_type == "99":
            exit(0)
        else:
            continue
        
    print(f"Using game data directory {base_path}\n")
    uma = umaModelReplace.UmaReplace(base_path)
    while True:
        do_type = input(
            "[1] Replace head model\n"
            "[2] Replace body model\n"
            "[3] Replace tail model (not recommended)\n"
            "[4] Replace head and body models\n"
            "[5] Modify character body texture\n"
            "[6] Replace gacha opening character\n"
            "[7] Replace skill animation\n"
            "[8] Replace G1 victory animation (experimental)\n"
            "[9] Unlock Live outfits\n"
            "[10] Clear all Live blur effects\n"
            "[11] Modify character head texture\n"
            "[97] Decrypt meta DB for querying\n"
            "[98] Restore all modifications\n"
            "[99] Exit\n"
            "Please select an option: "
        )

        if do_type == "1":
            print("Please enter a 7-character ID, e.g., 1046_01")
            uma.replace_head(input("Source ID: "), input("Target ID: "))
            print("Replacement complete")

        if do_type == "2":
            print("Please enter a 7-character ID, e.g., 1046_01")
            uma.replace_body(input("Source ID: "), input("Target ID: "))
            print("Replacement complete")

        if do_type == "3":
            checkDo = input(
                "Note: Currently you cannot replace tails across different models. "
                "The target character cannot appear at the same time as the original character.\n"
                "If you still want to proceed, enter y to continue: "
            )
            if checkDo not in ["y", "Y"]:
                continue
            print("Please enter a 4-digit ID, e.g., 1046")
            uma.replace_tail(input("Source ID: "), input("Target ID: "))
            print("Replacement complete")

        if do_type == "4":
            print("Please enter a 7-character ID, e.g., 1046_01")
            inId1 = input("Source ID: ")
            inId2 = input("Target ID: ")
            uma.replace_head(inId1, inId2)
            uma.replace_body(inId1, inId2)
            print("Replacement complete")

        if do_type == "5":
            print("Please enter a 7-character ID, e.g., 1046_01")
            replace_char_body_texture(uma, input("Character 7-character ID: "))

        if do_type == "6":
            print("Please enter the 6-digit outfit ID for the regular gacha opening animation, e.g., 100101 or 100130")
            uma.edit_gac_chr_start(input("Outfit 6-digit ID: "), '001')
            print("Please enter the 6-digit outfit ID for the chairman gacha opening animation, e.g., 100101 or 100130")
            uma.edit_gac_chr_start(input("Outfit 6-digit ID: "), '002')
            print("Replacement complete")

        if do_type == "7":
            print("Please enter the 6-digit character skill ID, e.g., 100101 or 100102")
            uma.edit_cutin_skill(input("Source ID: "), input("Target ID: "))

        if do_type == "8":
            checkDo = input(
                "Note: Some victory animations may cause audio glitches or black screens after replacement.\n"
                "If you still want to proceed, enter y to continue: "
            )
            if checkDo not in ["y", "Y"]:
                continue
            print("Please enter the 6-digit victory animation ID, e.g., 100101 or 100102")
            uma.replace_race_result(input("Source ID: "), input("Target ID: "))
            print("Replacement complete")

        if do_type == "9":
            uma.unlock_live_dress()
            print("Unlock complete")

        if do_type == "10":
            edit_live_id = input("Live ID (usually 4 digits; leave blank to modify all): ").strip()
            uma.clear_live_blur(edit_live_id)
            # Tip: This works best paired with the TLG plugin's Live free camera feature.
            # Repo: https://github.com/MinamiChiwa/Trainers-Legend-G

        if do_type == "11":
            print("Please enter a 7-character ID, e.g., 1046_01")
            replace_char_head_texture(uma, input("Character 7-character ID: "))

        if do_type == "97":
            uma.copy_meta(f"{os.getcwd()}/meta.db")
            print(f"Meta DB saved to {os.getcwd()}/meta.db")

        if do_type == "98":
            uma.file_restore()
            print("Modifications restored")

        if do_type == "99":
            break

        input("Press enter to continue...\n")
