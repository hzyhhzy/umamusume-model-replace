def get_body_mtl_names(_id):
    return [
        f"tex_bdy{_id}_shad_c",
        f"tex_bdy{_id}_base",
        f"tex_bdy{_id}_ctrl",
        f"tex_bdy{_id}_diff"
    ]


def get_body_mtl_path(_id):
    return f"sourceresources/3d/chara/body/bdy{_id}/materials/mtl_bdy{_id}"


def get_body_path(_id):
    return [
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}",
        get_body_mtl_path(_id)
    ]


def get_body_path_generic(_id):
    a= [
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_0_0_0",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_0_0_1",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_0_0_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_0_0_3",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_0_0_4",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_0_0",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_0_1",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_0_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_0_3",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_0_4",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_1_0",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_1_1",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_1_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_1_3",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_1_4",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_2_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_2_3",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_1_2_4",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_0_0",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_0_1",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_0_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_0_3",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_0_4",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_1_1",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_1_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_2_2",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_2_3",
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}_00_2_2_4",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust0_cloth00",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust0_cloth01",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust0_cloth02",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust0_cloth03",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust0_cloth04",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust1_cloth00",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust1_cloth01",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust1_cloth02",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust1_cloth03",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust1_cloth04",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust2_cloth00",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust2_cloth01",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust2_cloth02",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust2_cloth03",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust2_cloth04",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust3_cloth00",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust3_cloth01",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust3_cloth02",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust3_cloth03",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust3_cloth04",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust4_cloth00",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust4_cloth01",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust4_cloth02",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust4_cloth03",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_bust4_cloth04",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_cloth00",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_cloth01",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_cloth02",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_cloth03",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_cloth04",
        f"3d/chara/body/bdy{_id}/clothes/pfb_bdy{_id}_cloth04",
        get_body_mtl_path(_id)
    ]

    for i in range(4):
        if(i==0):
            tex_names=["base","ctrl","diff","shad_c","base_wet","ctrl_wet","diff_wet","shad_c_wet"]
        else:
            tex_names=["diff","shad_c","diff_wet","shad_c_wet"]
        for j in range(5):
            for tex_name in tex_names:
                a.append(f"3d/chara/body/bdy{_id}/textures/tex_bdy{_id}_00_{i}_{j}_{tex_name}")




    return a


def get_head_path(_id):
    return [
        f"3d/chara/head/chr{_id}/pfb_chr{_id}",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_cheek",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_eye",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_face",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_hair",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_mayu",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_tear",
        #f"sourceresources/3d/chara/head/chr{_id}/texture/tex_chr{_id}_cheek0",
        f"sourceresources/3d/chara/head/chr{_id}/facial/ast_chr{_id}_ear_target"
    ]

def get_head_path1(_id):
    return [
        f"3d/chara/head/chr{_id}/pfb_chr{_id}",
    ]

def get_tail1_path(_id):
    return [
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_diff",
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_diff_wet",
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_shad_c",
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_shad_c_wet",
    ]


def get_tail2_path(_id):
    return [
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_diff",
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_diff_wet",
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_shad_c",
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_shad_c_wet"
    ]


def get_gac_chr_start_path(type):
    return f"cutt/cutin/skill/gac_chr_start_{type}/gac_chr_start_{type}"


def get_cutin_skill_path(_id):
    return f"cutt/cutin/skill/crd{_id}_001/crd{_id}_001"


def get_race_result_path(_id):
    return get_chr_race_result_path(_id) + get_crd_race_result_path(_id)


def get_chr_race_result_path(_id):
    return [
        f"cutt/cutin/raceresult/res_chr{_id[:4]}_001/res_chr{_id[:4]}_001",
        f"3d/motion/raceresult/body/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001",
        f"3d/motion/raceresult/camera/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_cam",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_ear",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_ear_driven",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_face",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_face_driven"
    ]


def get_crd_race_result_path(_id):
    return [
        f"cutt/cutin/raceresult/res_crd{_id}_001/res_crd{_id}_001",
        f"3d/motion/raceresult/body/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001",
        f"3d/motion/raceresult/camera/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_cam",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_ear",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_ear_driven",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_face",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_face_driven",
        f"sound/v/snd_voi_race_{_id}.acb",
        f"sound/v/snd_voi_race_{_id}.awb"
    ]


def get_head_mtl_path(_id):
    return [
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_face",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_hair"
    ]
