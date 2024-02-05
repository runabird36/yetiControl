
import sys
if sys.platform.count("win"):
    import shotgun_api3
else:
    import general_md.shotgun_api3 as shotgun_api3
    

from general_md_3x import LUCY
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
import socket, json
import os, re
from pprint import pprint

milki_sg = None


class MilkiSgTk(QtCore.QObject):
    task_queried = QtCore.Signal(object)
    _tasks = None
    _c_task = {}
    _user = None
    _dialog = None


    def __init__(self):
        QtCore.QObject.__init__(self)
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._connect_sg)
        self.thread.start()

    def _connect_sg(self):
        global milki_sg
        '''
        Create Shotgun instance with connecting
        Return
            shotgun instance
        '''
        SERVER_PATH = 'https://giantstep.shotgunstudio.com'
        SCRIPT_NAME = 'milki'
        SCRIPT_KEY = 'a7havEuespharhhnozxt~lncd'

        try:
            if 'NUKE' in socket.gethostname():
                print('NUKE PROXY')
                milki_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='proxy2.giantstep.net:9098')
            elif socket.gethostname() in ['Graphics-M-KDH']:
                milki_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='proxy2.giantstep.net:9098')
            else:
                print('3D CGI PROXY')
                milki_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='proxy1.giantstep.net:9098')
        except:
            print('NONE PROXY')
            milki_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='')


    def showdialog(self):
        self._dialog = QtGui.QDialog()
        self._dialog.setWindowTitle("Dialog")
        self._dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self._dialog.show()


    def _get_sg(self):
        global milki_sg
        if milki_sg is None:
            self._connect_sg()

        return milki_sg

    def _set_user(self):
        host = socket.gethostname()

        if host == '3DCGI-LT-PJH':
            ip_of_host = socket.gethostbyname(host)
            if ip_of_host == '192.168.10.122':
                host = '3DCGI-LT-PJH2'
            else:
                host = '3DCGI-LT-PJH'
        elif host == 'PD-2B-5F-PUBLIC':
            host = '3DCGI-TD-STY'
        elif host == "client01":
            host = "3DCGI-PIP-CSW"
        elif host == "client02":
            host = "3DCGI-PIP-CSW"
        u_filter = [['sg_host_name', 'is', host]]
        u_fields = ['name', 'user', 'id']
        self._user = self._get_sg().find_one('HumanUser', u_filter, u_fields)

    def get_user(self):
        return self._user

    def _find_tasks(self, prj, entity_name, ):
        t_filter = []
        t_filter.append(['project', 'name_is', prj])
        t_filter.append(['entity', 'name_is', entity_name])
        # t_filter.append(['sg_status_list', 'in',  ['none', 'wtg', 'rdy', 'ip', 'pub', 'gfn', 'apr', 'retake', 'prepub', 'final']])
        t_field = ['content', 'sg_sort_order', 'sg_status_list', 'entity', 'task_assignees', 'project', 'step.Step.code', 'entity.Asset.assets', 'entity.Asset.parents']
        tasks = self._get_sg().find('Task', t_filter, t_field)
        for task in tasks:
            assignees = task['task_assignees']
            if assignees is None:
                continue
            name_list = []
            for user in assignees:
                name_list.append(user['name'])
            task['assignee_names'] = name_list
        return tasks


    def get_task(self, prj, entity_name, step, scene_type):
        if self._user is None:
            self._set_user()
        if self._tasks is None:
            self._tasks = self._find_tasks(prj, entity_name)
        
        _c_sort_order = ''
        for task in self._tasks:
            # pprint(task)
            assignee_names = task['assignee_names']
            task_step = task['step.Step.code'].lower()
            sort_order = task['sg_sort_order']
            # sub_asset_list = task['entity.Asset.assets']
            # parent_asset_list = task['entity.Asset.parents']
            # 2020-04-08 updated
            # Check is subasset / parent asset / shot
            # _type_flag = 'ASSET_PARENT'
            # if scene_type == 'sequence':
            #     _type_flag = 'SHOT'
            # elif scene_type == 'assets':
            #     if sub_asset_list == [] and parent_asset_list !=  []:
            #         _type_flag = 'ASSET_SUB'
            #     elif sub_asset_list != [] and parent_asset_list ==  []:
            #         _type_flag = 'ASSET_PARENT'
            if assignee_names is None:
                continue
            if self._user['name'] in assignee_names and task_step == step:
                
                # 2020-04-08 updated
                # Case :
                #     In case parent asset name and sub asset name are same (eggTart, eggTart) ,
                #     when publish, two tasks which are name same each other is queried
                #     and tool is confused about which one is correct
                # if scene_type == 'Asset':
                #     if _is_subAsset == True and _type_flag == 'ASSET_PARENT' or\
                #         _is_subAsset == True and _type_flag == 'SHOT':
                #         print('Pass!')
                #         continue
                if _c_sort_order == '':
                    
                    _c_sort_order = sort_order
                    self._c_task = task
                else:
                    if _c_sort_order < sort_order:
                        
                        _c_sort_order = sort_order
                        self._c_task = task

        self.task_queried.emit(self._c_task)

    def create_new_sg_pubfiles(self, paths, thumb, desc = '', change_sg_status=True, scene_ver='', pipe_step=''):
        if self._c_task is {}:
            raise Exception("Task is none")
        if sys.platform.count("win"):
            j_path = "Z:/backstage/maya/milki/docs/publish_types.json"
        else:
            j_path = "/usersetup/linux/scripts/maya_sc/milki/docs/publish_types.json"
        j_data = open(j_path, 'r').read()
        pub_types = json.loads(j_data)
        pub_info = {}
        pub_info['project'] = self._c_task['project']

        pub_info['entity'] = self._c_task['entity']
        
        pub_info['created_by'] = self._user
        pub_info['updated_by'] = self._user

        assignee_names = self._c_task['assignee_names']
        del (self._c_task['assignee_names'])
        pub_info['task'] = self._c_task
        pub_info['description'] = desc
        if scene_ver != '':
            if scene_ver.startswith("v"):
                dev_ver = int(scene_ver.replace("v", ""))
            pub_info['version_number'] = dev_ver
        else:
            tarpath = LUCY.get_full_path()
            res = re.search(r"v\d+(3)\.[a-zA-Z]+$", tarpath)
            if res:
                temp_info = res.group()
                vernum = temp_info.split(".")[0]
                dev_ver = int(vernum.replace("v", ""))
                pub_info['version_number'] = dev_ver

                
        if pipe_step != '':
            pub_info['sg_published_pipe_step'] = pipe_step
        pub_id_list = []
        for file_path in paths:
            file_name = os.path.basename(file_path)
            pub_info['code'] = file_name

            url = 'file:///{0}'.format(file_path)
            path_dic = {'content_type' : None, 'type' : 'Attatchment'}

            path_dic['name']        = file_name
            path_dic['url']         = url
            pub_info['path']        = path_dic
            pub_info['path_cache']  = file_path
            ext = os.path.splitext(file_path)[-1]
            pub_info['published_file_type'] = pub_types.get(ext.lower(), None)
            sg_pub_file = self._get_sg().create('PublishedFile', pub_info)
            if sg_pub_file is None:
                continue
            pub_id = sg_pub_file['id']
            pub_id_list.append(str(pub_id))
            if os.path.exists(thumb):
                try:
                    self._get_sg().upload_thumbnail('PublishedFile', pub_id, thumb)
                    if pub_info['entity']['type'] == 'Asset':
                        self._get_sg().upload_thumbnail('Asset', pub_info['entity']['id'], thumb)
                except Exception as e:
                    print(str(e))
                    pass
            self.create_pub_note(file_name, desc)
        if change_sg_status == True:
            self._c_task['assignee_names'] = assignee_names
            status = {"sg_status_list" : 'pub'}
            self._get_sg().update('Task', self._c_task['id'], status)
        return pub_info['project'], pub_id_list


    def set_prepub_status(self):
        '''
        Change status of task
        '''
        status = {"sg_status_list" : "prepub"}
        res = self._get_sg().update('Task', self._c_task['id'], status)
        if res is None:
            raise Exception ("SG Tk Error")


    def create_pub_note(self, file_name, desc):
        divide = '-'*40
        note_content = "{0}\nPUBLISH NOTE\n{1}\n".format(divide, divide)

        infos = []
        infos.append(('Project', self._c_task['project']['name']))
        infos.append(('Task', self._c_task['content']))
        infos.append(('User', self._user['name']))
        infos.append(('Link', self._c_task['entity']['name']))
        infos.append(('File Name', file_name))

        for info in infos:
            title = info[0]
            content = info[1]
            infoStr = '{0} : {1}\n'.format(title, content)
            note_content += infoStr
        note_content += 'Comment : '

        
        note_content += desc

        note =  {}
        note["content"] = note_content
        note["project"] = self._c_task['project']
        note["user"] = self._user
        note["note_links"] = [self._c_task['entity']]
        note["addressings_to"] = self._get_to_users()

        self._get_sg().create('Note', note)


    def _get_to_users(self):
        to_users = []

        if self._user is None:
            self._set_user()

        if self._tasks is None or len(self._tasks) == 0:
            raise Exception ("No Tasks")

        for task in self._tasks:
            assignees = task['task_assignees']
            if assignees is None:
                continue
            to_users.extend(assignees)
        return to_users


    def upload_version(self, version_path, desc):
        version_name = os.path.basename(version_path)
        ver_dic = {'code': version_name,
            'entity': self._c_task['entity'],
            'sg_status_list': 'rev',
            'sg_path_to_movie' : version_path,
            'user': self._user,
            'sg_task' : self._c_task,
            'created_by' :self._user,
            'project': self._c_task['project']
            }
        description = "Scene : {0}\n\nComment : ".format(LUCY.get_full_path())
        
        description += desc
        ver_dic['description'] = description
        version = self._get_sg().create('Version', ver_dic)

        if version is None:
            raise Exception("Fail to create verion cause of shotgun api problem")

        ver_id = version['id']

        #upload version
        self._get_sg().upload('Version', ver_id, version_path, field_name='sg_uploaded_movie')
