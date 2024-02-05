import os, sys, time, re
import json, traceback


_path = os.getcwd()
if _path not in sys.path:
    sys.path.append(_path)

import YBB_path_module







JOB_NUM = ""


def write_log(input_str :str) -> None:
    err_path = "/home/taiyeong.song/Desktop/pipeTemp/yetiFurBakeryBatch/resource/testData/err_log.md"
    with open(err_path, "w") as f:
        f.write(input_str)


def logger(func):
    def wrapper(*args, **kwargs):
        global JOB_NUM
        try:
            res = func(*args, **kwargs)
            return res
        except:
            write_log(traceback.format_exc() + JOB_NUM)
            sys.stderr.write(traceback.format_exc())
            sys.exit()
    return wrapper



def flush_then_wait():
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(2)



def convert_to_convention_name(baked_filename :str) -> str:
    
    
    fname, ext      = os.path.splitext(baked_filename)
    frame_num       = fname.split(".")[-1]
    f_real_name     = fname.split(".")[0]
    fname_components= f_real_name.split("_")

    assetname       = fname_components[0]
    NAME_components = fname_components[1:-2]
    NAME            = "_".join(NAME_components)
    last_word       = fname_components[-1]
    search_res = re.search(r"\d{3}", last_word)
    if search_res:
        ns_num = search_res.group()
    else:
        ns_num = "001"

    
    return f"{assetname}_{ns_num}_{NAME}.{frame_num}.fur"





def run_process() -> None:
    global JOB_NUM

    args                = sys.argv[1:]
    job_num             = args[0]
    upload_info         = args[1]
    job_info_dict       = json.loads(upload_info)
    maya_scene_path     = args[2]

    # print(job_info_dict)
    
    s_frame             = job_info_dict.get("Start_Frame")
    e_frame             = job_info_dict.get("End_Frame")
    sample              = job_info_dict.get("Sample")
    output_dir          = job_info_dict.get("Out_Dir")
    vernum              = job_info_dict.get("Vernum")

    output_dir_with_vernum = f"{output_dir}/{vernum}"
    if os.path.exists(output_dir_with_vernum) == False:
        os.makedirs(output_dir_with_vernum)

    if job_info_dict.get("With_Scene_Info") == True:
        mel_elements = ["\"loadPlugin \\\"pgYetiMaya.so\\\";",
                            "select \\`ls -l -type \\\"pgYetiMaya\\\"\\`;"
                            f"pgYetiCommand -writeCache \\\"{output_dir_with_vernum}/<NAME>.%04d.fur\\\" -range \\`playbackOptions -q -min\\` \\`playbackOptions -q -max\\` -samples {sample};\""]
    else:
        mel_elements = ["\"loadPlugin \\\"pgYetiMaya.so\\\";",
                            "select \\`ls -l -type \\\"pgYetiMaya\\\"\\`;"
                            f"pgYetiCommand -writeCache \\\"{output_dir_with_vernum}/<NAME>.%04d.fur\\\" -range {s_frame} {e_frame} -samples {sample};\""]

    mel_command = " ".join(mel_elements)

    cmd_elements = [
                        YBB_path_module.MAYA_EXE_PATH,
                        "-batch",
                        "-file",
                        maya_scene_path,
                        "-command",
                        mel_command
                    ]

    bake_cmd = " ".join(cmd_elements)

    print(bake_cmd)
    res = os.system(bake_cmd)
    sys.stdout.write(f"Job Num : {job_num}\nTotal complete: 50%\n")
    flush_then_wait()






    
    for fur_fname in os.listdir(output_dir_with_vernum):
        fname, ext = os.path.splitext(fur_fname)
        if ext in [".fur"]:
            converted_name = convert_to_convention_name(fur_fname)
            
            os.rename(f"{output_dir_with_vernum}/{fur_fname}", f"{output_dir_with_vernum}/{converted_name}")
            

    
    

    sys.stdout.write(f"Job Num : {job_num}\nTotal complete: 100%\n")
    flush_then_wait()
    

run_process()




    

