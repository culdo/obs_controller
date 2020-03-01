from multiprocessing.managers import BaseManager, NamespaceProxy


class OBSController(BaseManager):
    pass


class Command:
    def __init__(self):
        self.state = None


cmd = Command()
obs_controller = OBSController(('127.0.0.1', 50000), authkey=b'obs_controller')


def get_cmd():
    return cmd


def start_server(initial_state):
    OBSController.register("get_cmd", get_cmd, NamespaceProxy)
    obs_controller.start()
    shared_cmd = obs_controller.get_cmd()
    shared_cmd.state = initial_state
    return shared_cmd


def start_client():
    OBSController.register("get_cmd", proxytype=NamespaceProxy)
    while True:
        try:
            obs_controller.connect()
            break
        except ConnectionRefusedError:
            print("Wait server connection. Retry...")

    return obs_controller.get_cmd()
