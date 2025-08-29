import umaModelReplace

uma = umaModelReplace.UmaReplace()

debug_auto=True
debug_auto=False

def replace_char_body_texture(char_id: str):
    is_not_exist, msg = uma.save_char_body_texture(char_id, False)
    if not is_not_exist:
        print(f"解包资源已存在: {msg}")
        do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
        if do_replace in ["Y", "y"]:
            _, msg = uma.save_char_body_texture(char_id, True)

    print(f"已尝试导出资源, 请查看目录: {msg}")
    do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                   "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                   "请输入: ")
    if do_fin.strip() in ["Y", "y"]:
        uma.replace_char_body_texture(char_id)
        print("贴图已修改")

def replace_char_head_texture(char_id: str):
    for n, i in enumerate(uma.save_char_head_texture(char_id, False)):
        is_not_exist, msg = i

        if not is_not_exist:
            print(f"解包资源已存在: {msg}")
            do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
            if do_replace in ["Y", "y"]:
                _, msg = uma.save_char_head_texture(char_id, True, n)[0]

        print(f"已尝试导出资源, 请查看目录: {msg}")

    do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                   "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                   "请输入: ")
    if do_fin.strip() in ["Y", "y"]:
        uma.replace_char_head_texture(char_id)
        print("贴图已修改")


if __name__ == "__main__":
    
    print("当前版本：2025.8.30")
    print("开源代码：https://github.com/hzyhhzy/umamusume-model-replace")
    print("")
    while True:
        input_instr_str="[1] 更换头部模型\n"\
                        "[2] 更换身体模型\n"\
                        "[3] 更换尾巴模型(不建议)\n"\
                        "[4] 更换头部与身体模型\n"\
                        "[5] 修改角色身体贴图\n"\
                        "[6] 更换抽卡开门人物\n"\
                        "[7] 更换技能动画\n"\
                        "[8] 更换G1胜利动作(实验性)\n"\
                        "[9] Live服装解锁\n"\
                        "[10] 清除Live所有模糊效果\n"\
                        "[11] 修改角色头部贴图\n"\
                        "[21] 替换通用服装\n"\
                        "[98] 复原所有修改\n"\
                        "[99] 退出\n"\
                        "请选择您的操作: "
                        
        input_instr_str=\
                        "----------------------------\n"\
                        "功能列表\n"\
                        "----------------------------\n"\
                        "[4] 更换头部与身体模型\n"\
                        "[21] 替换通用服装\n"\
                        "[98] 复原所有修改\n"\
                        "[99] 退出\n"\
                        "[1] 更换头部模型\n"\
                        "[2] 更换身体模型\n"\
                        "----------------------------\n"\
                        "以下功能年久失修，不保证能用：\n"\
                        "----------------------------\n"\
                        "[3] 更换尾巴模型(不建议)\n"\
                        "[5] 修改角色身体贴图\n"\
                        "[6] 更换抽卡开门人物\n"\
                        "[7] 更换技能动画\n"\
                        "[8] 更换G1胜利动作(实验性)\n"\
                        "[9] Live服装解锁\n"\
                        "[10] 清除Live所有模糊效果\n"\
                        "[11] 修改角色头部贴图\n"\
                        "请选择您的操作: "
        do_type = "1" if debug_auto else input(input_instr_str)

        if do_type == "1":
            print("请输入7位数ID, 例: 1024_00。（不知道ID就去Umaviewer里找）")
            if(debug_auto):
                uma.replace_head("1024_00", "9002_00")
            else:
                uma.replace_head(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "2":
            print("请输入7位数ID, 例: 1024_00（不知道ID就去Umaviewer里找）")
            if(debug_auto):
                uma.replace_body("1024_00", "9002_00")
            else:
                uma.replace_body(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "3":
            checkDo = input("注意: 目前无法跨模型更换尾巴, 更换目标不能和原马娘同时出场。\n"
                            "若您仍要更改, 请输入y继续: ")
            if checkDo not in ["y", "Y"]:
                continue
            print("请输入4位数ID, 例: 1046")
            uma.replace_tail(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "4":
            print("请输入7位数ID, 例: 1024_00（不知道ID就去Umaviewer里找）")

            inId1 = input("替换ID: ")
            inId2 = input("目标ID: ")
            uma.replace_head(inId1, inId2)
            uma.replace_body(inId1, inId2)
            print("替换完成")

        if do_type == "5":
            print("请输入7位数ID, 例: 1024_00（不知道ID就去Umaviewer里找）")
            replace_char_body_texture(input("角色7位ID: "))

        if do_type == "6":
            print("请输入普通开门动画的人物服装6位数ID, 例: 100101、100130")
            uma.edit_gac_chr_start(input("服装6位数ID: "), '001')
            print("请输入理事长开门动画的人物服装的6位数ID, 例: 100101、100130")
            uma.edit_gac_chr_start(input("服装6位数ID: "), '002')
            print("替换完成")

        if do_type == "7":
            print("请输入人物技能6位数ID, 例: 100101、100102")
            uma.edit_cutin_skill(input("替换ID: "), input("目标ID: "))

        if do_type == "8":
            checkDo = input("注意: 目前部分胜利动作替换后会出现破音、黑屏等问题。\n"
                            "若您仍要更改, 请输入y继续: ")
            if checkDo not in ["y", "Y"]:
                continue
            print("请输入胜利动作6位数ID, 例: 100101、100102")
            uma.replace_race_result(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "9":
            uma.unlock_live_dress()
            print("解锁完成")

        if do_type == "10":
            edit_live_id = input("Live id (通常为4位, 留空则全部修改): ").strip()
            uma.clear_live_blur(edit_live_id)
            # print("此功能搭配TLG插件的Live自由镜头功能，使用效果更佳\n"
            #       "This function is paired with the TLG plug-in's Live free camera for better use\n"
            #       "Repo: https://github.com/MinamiChiwa/Trainers-Legend-G")

        if do_type == "11":
            print("请输入7位数ID, 例: 1024_00")
            replace_char_head_texture(input("角色7位ID: "))

        if do_type == "21":
            print("请输入7位数ID, 例: 0050_00, 0051_00, 0004_00（泳装）, 0004_01（浴巾）（不知道ID就去Umaviewer里找）")
            uma.replace_body_generic(input("被替换ID: "), input("目标ID: "))

            print("替换完成")

        if do_type == "98":
            uma.file_restore()
            print("已还原修改")

        if do_type == "99":
            break

        input("Press enter to continue...\n")
