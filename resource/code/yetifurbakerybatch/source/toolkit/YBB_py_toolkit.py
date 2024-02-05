from PyQt5.QtCore import QThread, pyqtSignal, qDebug, QProcess
# from modules.sg_mod import SG

import os, re
import queue
from functools import partial
from YBB_path_module import (BAKE_FUR_PROCESS_SCRIPT, PYTHON_COMPILER_PATH)
from pprint import pprint



def find_files(root_dir, file_extension):
    matches = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(file_extension):
                file_path = os.path.join(dirpath, filename)
                matches.append(file_path)
    return matches



class Worker(QThread):
    JOB_FINISHED = pyqtSignal()
    DEL_SELF     = pyqtSignal()
    def __init__(self) -> None:
        super(Worker, self).__init__()

    def set_job(self, func, *args, **kwargs) -> None:
        self.func   = func
        self.args   = args
        self.kwargs = kwargs

    def run(self) -> None:
        self.func(*self.args, **self.kwargs)
        self.JOB_FINISHED.emit()



class SingleProcess():
    __PROCESS__ = QProcess()

    @property
    def PROCESS(self) -> QProcess:
        return self.__PROCESS__



class ProcessPool():
    __POOL__            = queue.Queue()
    standby_pool        = {}
    concurrency_count   = 4

    @property
    def POOL(self) -> queue.Queue:
        return self.__POOL__
    
    @POOL.setter
    def POOL(self, _pool) -> None:
        self.__POOL__ = _pool

    @property
    def CONCURRENT_COUNT(self) -> None:
        return self.concurrency_count
    
    @CONCURRENT_COUNT.setter
    def CONCURRENT_COUNT(self, count :int) -> int:
        self.concurrency_count = count
        
    def message(self, txt :str) -> None:
        print(txt)

    def update_progress(self, job_num :str) -> None:
        progress_re = re.compile("Total complete: (\d+)%")

        def simple_percent_parser(output):
            """
            Matches lines using the progress_re regex,
            returning a single integer for the % progress.
            """
            m = progress_re.search(output)
            if m:
                pc_complete = m.group(1)
                return int(pc_complete)
            else:
                return None
            

        data = self.standby_pool.get(job_num).get_process().readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        

        cur_percentage = simple_percent_parser(stdout)
        if cur_percentage == None:
            self.message(stdout)
            return

        self.standby_pool.get(job_num).update_progress(cur_percentage)

    def change_process_status(self, job_num :str) -> None:
        data = self.standby_pool.get(job_num).get_process().readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)
        self.standby_pool.get(job_num).PROCESS_STATUS = "ERROR"
        self.standby_pool.get(job_num).set_log(stderr)
        self.standby_pool.get(job_num).change_status_gif("ERROR")
        self.standby_pool.get(job_num).get_process().terminate()
        

    def add_process(self, input_process :object) -> None:
        print(f"Add : {input_process.JOB_NUM}")
        self.POOL.put(input_process)


    def update_standby(self, finished_jobnum :str) -> None:
        print(f"Finished process :{finished_jobnum}")
        finished_process = self.standby_pool.get(finished_jobnum)
        if finished_process.PROCESS_STATUS == "ERROR":
            return
        finished_process.PROCESS_STATUS = "FINISHED"
        finished_process.change_status_gif("CLEAR")
        del self.standby_pool[finished_jobnum]

        if self.POOL.empty() == False:
            next_process = self.POOL.get()
            self.standby_pool.update({next_process.JOB_NUM : next_process})
            self.run_process(next_process)
        # self.POOL.task_done()

    def run_process(self, tar_process :object) -> None:
        print(f"Start process : {tar_process.JOB_NUM}")
        tar_process.change_status_gif("START")
        if tar_process.get_process().receivers(tar_process.get_process().finished) <= 0 :
            tar_process.get_process().readyReadStandardOutput.connect(partial(self.update_progress, tar_process.JOB_NUM))
            # tar_process.get_process().readyReadStandardError.connect(partial(self.change_process_status, tar_process.JOB_NUM))
            tar_process.get_process().finished.connect(partial(self.update_standby, tar_process.JOB_NUM))
        tar_process.get_process().start(PYTHON_COMPILER_PATH, [BAKE_FUR_PROCESS_SCRIPT, tar_process.JOB_NUM, tar_process.JOB_INFO, tar_process.FROM_PATH])

    def run(self):
        def init_standby_pool() -> None:
            for _idx in range(self.CONCURRENT_COUNT):
                if self.POOL.empty():
                    break
                tar_process = self.POOL.get()
                self.standby_pool.update({tar_process.JOB_NUM : tar_process})

        print(f"Run Pool")
        init_standby_pool()
        

        for job_num , standby_process in self.standby_pool.items():
            self.run_process(standby_process)
            
        

    def clear_all(self) -> None:
        self.__POOL__            = queue.Queue()
        self.standby_pool        = {}



