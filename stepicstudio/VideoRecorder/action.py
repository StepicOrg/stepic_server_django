from stepicstudio.models import UserProfile, CameraStatus, Lesson, Step, SubStep, Course
from stepicstudio.FileSystemOperations.action import *
from stepicstudio.const import *
from stepicstudio.ssh_connections.screencast import *
from STEPIC_STUDIO.settings import XML_SETTINGS_DIR
from stepicstudio.const import SUBSTEP_PROFESSOR
import time


def start_recording(**kwargs):
    user_id = kwargs["user_id"]
    folder_path = kwargs["serverFilesFolder"].serverFilesFolder
    data = kwargs["data"]
    generate_xml(XML_SETTINGS_DIR, substep_server_path(folder_path=folder_path, data=data), SUBSTEP_PROFESSOR)
    add_file_to_test(folder_path=folder_path, data=data)
    server_status = run_adobe_live()
    screencast_status = ssh_screencast_start()
    db_camera = CameraStatus.objects.get(id="1")
    if server_status and screencast_status:
        if not db_camera.status:
            db_camera.status = True
            db_camera.start_time = int(round(time.time() * 1000))
            db_camera.save()
        return True
    else:
        return False

def delete_substep_files(**kwargs):
    folder_path = kwargs["serverFilesFolder"].serverFilesFolder
    data = kwargs["data"]
    return delete_substep_on_disc(folder_path=folder_path, data=data)


def delete_step_files(**kwargs):
    folder_path = kwargs["serverFilesFolder"].serverFilesFolder
    data = kwargs["data"]
    return delete_step_on_disc(folder_path=folder_path, data=data)



def files_update(**kwargs):
    files_txt_update(**kwargs)
    return True


#TODO: REMAKE! Wrong implementation
def stop_cam_recording():
    camstat = CameraStatus.objects.get(id="1")
    camstat.status = False
    ssh_screencast_stop()
    camstat.save()
    stop_adobe_live()


def delete_files_associated(url_args):
    lesson_id = int(url_args[url_args.index(COURSE_ULR_NAME)+3])
    folder_on_server = Lesson.objects.get(id=lesson_id).os_path
    return delete_files_on_server(folder_on_server)
