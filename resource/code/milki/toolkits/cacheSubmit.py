# encoding=utf-8

import maya.cmds as cmds
import os, sys, re
import subprocess
import time
import shutil
import tempfile
from general_md_3x import LUCY

repository_path = ""
def run_cmd(cmd_str):
    pipes = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = pipes.communicate()

    std_err.decode('cp949')

    _res = std_out.decode('cp949')
    _res02= pipes.poll()
    # return std_err
    return str(_res)


def get_repository_path():
    global repository_path
    if repository_path == "":
        if sys.platform == "win32":
            _res = run_cmd("C:\\PROGRA~1\\Thinkbox\\Deadline10\\bin\\deadlinecommand GetRepositoryRoot")
        else:
            _res = run_cmd("/opt/Thinkbox/Deadline10/bin/deadlinecommand GetRepositoryRoot")
        repository_path = _res
        return _res
    else:
        return repository_path


def is_to_linux_farm():
    global repository_path
    if "gtserver" in get_repository_path():
        print("Current Repository : {0}".format(repository_path))
        return True
    else:
        return False


def create_job_file(mel_path, ma_path, number):
    full_path = LUCY.get_full_path()
    dir_path = os.path.dirname(full_path)
    build = cmds.about(x64=1)
    if cmds.about(x64=1):
        build = '64bit'
    else:
        build = '32bit'

    job =  'Renderer=mayaSoftware\n'\
           'ProjectPath={0}\n'\
           'UsingRenderLayers=0\n'\
           'StrictErrorChecking=0\n'\
           'Version={1}\n'\
           'Build={2}\n'\
           'SceneFile={3}\n'\
           'IgnoreError211=0\n'\
           'StartupScript={4}\n'\
           'AntiAliasing=low'.format(
               dir_path
              , cmds.about(v=1)
              , build
              , ma_path
              , mel_path)

    job_path = '{0}/maya_deadline_job_{1}.job'.format(tempfile.gettempdir(), number)
    with open(job_path, 'w') as job_file:
        job_file.write(job)

    return job_path



def create_job_file_only_script_job(mel_path, ma_path, number):
    full_path = LUCY.get_full_path()
    dir_path = os.path.dirname(full_path)

    build = cmds.about(x64=1)
    if cmds.about(x64=1):
        build = '64bit'
    else:
        build = '32bit'

    job =  'ProjectPath={0}\n'\
           'StrictErrorChecking=0\n'\
           'Version={1}\n'\
           'Build={2}\n'\
           'SceneFile={3}\n'\
           'ScriptJob=True\n'\
           'ScriptFilename={4}\n'\
           'UseLegacyRenderLayers=0\n'\
           'RenderSetupIncludeLights=0\n'\
           'AntiAliasing=low'.format(
               dir_path
              , cmds.about(v=1)
              , build
              , ma_path
              , mel_path)

    job_path = '{0}/maya_deadline_job_{1}.job'.format(tempfile.gettempdir(), number)
    with open(job_path, 'w') as job_file:
        job_file.write(job)

    return job_path




def copy_thumb(abc_path, thumb):
    '''
        Copy to thumbnail file

        Args:
            thumb (string) : get thumbnail image path
            sceneName (string) : get copy SceneFile Name

        Return:
            string : new Thumbnail path
    '''
    pub_dir = os.path.dirname(abc_path)
    thumb_name = os.path.basename(thumb)

    new_path = pub_dir+"/Thumbnail/"
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    new_thumb = new_path + thumb_name
    try:
        shutil.copy2(thumb, new_thumb)
        return new_thumb
    except Exception as e:
        print('Thumb copy error')
        print(str(e))
        return ''


def create_batch_name(file_name):
    batch_name = ''
    version_finder = re.compile('v\d+')
    ver = version_finder.search(file_name)
    if ver is None:
        batch_name = file_name

    ver_str = ver.group()
    try:
        ver_idx = file_name.find(ver_str)
        batch_name = file_name[:ver_idx-1]
    except Exception as e:
        print(str(e))

    return batch_name.encode('utf-8')


def get_version_of_file(file_name):
    version_finder = re.compile('v\d+')
    ver = version_finder.search(file_name)
    if ver is None:
        return None

    return ver.group()

def extract_root(abc_path):
    abc_file = os.path.splitext(abc_path)[0]
    abc_split = abc_file.split('_')
    version = get_version_of_file(abc_file)

    root = '_'.join(abc_split[-2:])
    if not version is None:
        root = '{0}_{1}'.format(root, version)

    return root

def create_info(abc_path, task, user, thumb, desc, number, cachetype='abc'):
    #extra 0 = copy scenePath
    #extra 1 = sceneName
    file_split = os.path.basename(LUCY.get_full_path()).split('_')
    file_name = '_'.join(file_split)

    thumb = copy_thumb(abc_path, thumb)
    thumb = thumb.replace("/", "\\")

    batch_name = create_batch_name(file_name)
    if cachetype == "ass":
        comment = "ASS cache File"
        machine_group = "arnold"
    else:
        comment = "Alembic Cache File"
        # machine_group = "abc_cache_export"
        machine_group = "cache"
    
    try:
        info = 'Plugin=MayaBatch\n'\
            'Name={0}\n'\
            'Comment={10}\n'\
            'Priority=99\n'\
            'ConcurrentTasks=1\n'\
            'Department=Animation\n'\
            'Group={9}\n'\
            'Frames=1\n'\
            'ChunkSize=9999\n'\
            'ExtraInfo0={1}\n'\
            'ExtraInfo1={2}\n'\
            'ExtraInfo2={3}\n'\
            'ExtraInfo3={4}\n'\
            'ExtraInfo4={5}\n'\
            'ExtraInfo5=Alembic\n'\
            'ExtraInfo6={6}\n'\
            'ExtraInfo7={7}\n'\
            'BatchName={8}\n'.format(
                extract_root(abc_path)
                , abc_path
                , os.path.dirname(abc_path)
                , LUCY.get_full_path()
                , thumb
                , desc
                , task
                , user
                , batch_name
                , machine_group
                , comment
                )
        info_path = '{0}/maya_deadline_info_{1}.job'.format(tempfile.gettempdir(), number)
        with open(info_path, 'w') as info_file:
            info_file.write(info)
    except Exception as e:
        info = 'Plugin=MayaBatch\n'\
            'Name={0}\n'\
            'Comment={10}\n'\
            'Priority=99\n'\
            'ConcurrentTasks=1\n'\
            'Department=Animation\n'\
            'Group={9}\n'\
            'Frames=1\n'\
            'ChunkSize=9999\n'\
            'ExtraInfo0={1}\n'\
            'ExtraInfo1={2}\n'\
            'ExtraInfo2={3}\n'\
            'ExtraInfo3={4}\n'\
            'ExtraInfo4={5}\n'\
            'ExtraInfo5=Alembic\n'\
            'ExtraInfo6={6}\n'\
            'ExtraInfo7={7}\n'\
            'BatchName={8}\n'.format(
                extract_root(abc_path)
                , abc_path
                , os.path.dirname(abc_path)
                , LUCY.get_full_path()
                , thumb
                , desc.encode('utf8')
                , task
                , user
                , batch_name
                , machine_group
                , comment
                )
        info_path = '{0}/maya_deadline_info_{1}.job'.format(tempfile.gettempdir(), number)
        with open(info_path, 'w') as info_file:
            info_file.write(info)


    return info_path



def create_mel_file(mel_dir, command, number, cachetype='abc'):
    current_time = time.localtime(time.time())
    c_time = "{0:0=4}{1:0=2}{2:0=2}{3:0=2}{4:0=2}{5:0=2}".format(current_time.tm_year
                                                                ,current_time.tm_mon
                                                                ,current_time.tm_mday
                                                                ,current_time.tm_hour
                                                                ,current_time.tm_min
                                                                ,current_time.tm_sec)
    mel_path = '{0}/alembicMelScript_{1}_{2}.mel'.format(mel_dir, c_time, number)
    _plugin_check_mel = "string $res=\"\";$res = `pluginInfo -query -loaded \"AbcExport\"`;if ($res == \"0\"){loadPlugin(\"AbcExport.mll\");};"


    if is_to_linux_farm() == True and "X:/" in command:
            command = command.replace("X:/projects", "/projects")
    if cachetype == 'ass':
        export_mel = command
    else:
        export_mel = "AbcExport -j \"{0}\";".format(command)
        export_mel = _plugin_check_mel + export_mel
        
    with open(mel_path, 'w') as mel_file:
        mel_file.write(export_mel)
    if sys.platform.count("win"):
        mel_path = mel_path.replace('/', '\\')
    if '\\' in mel_path:
        mel_path = mel_path.replace('\\', '/')
    if is_to_linux_farm() == True:
        mel_path = mel_path.replace('X:/projects', '/projects')
    return str(mel_path)


def submit_to_farm(cmd_info, mel_path, ma_path, task, user, thumb, desc, cache_type="abc"):
    """
    {path:command}
    """
    mel_dir = os.path.dirname(mel_path)
    if not os.path.exists(mel_dir):
        os.mkdir(mel_dir)

    num = 0
    for abc_path, command in cmd_info.items():
        print('command : ' + str(command))
        mel_path = create_mel_file(mel_dir, command, num, cache_type)
        job_path = create_job_file_only_script_job(mel_path, ma_path, num)
        info_path = create_info(abc_path, task, user, thumb, desc, num, cache_type)
        num += 1
        if sys.platform == "win32":
            submit_command = "C:\\PROGRA~1\\Thinkbox\\Deadline10\\bin\\deadlinecommand \"{0}\" \"{1}\"".format(info_path, job_path)
        else:
            submit_command = "/opt/Thinkbox/Deadline10/bin/deadlinecommand \"{0}\" \"{1}\"".format(info_path, job_path)
        print(submit_command)
        subprocess.Popen(submit_command, shell = True)
