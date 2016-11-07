from app import BaseApp
import config


class AppManager(object):

    def __init__(self):
        self.logger = config.get_logger().getChild(
            __name__ + "." + self.__class__.__name__)
        self.app_dict = {}

    def add_apps(self, app_args):
        if not isinstance(app_args, list):
            raise TypeError("Argument should be type of list")
        for app_arg in app_args:
            if not isinstance(app_arg, tuple):
                raise TypeError("Element of argument should be tuple")
            self.add_app(*app_arg)

    def add_app(self, app_id, proj_dir, package):
        app = BaseApp(proj_dir, package)
        self.logger.info("Add app " + str(app))
        self.app_dict[app_id] = app

    def get_app(self, find_app_id):
        if find_app_id not in self.app_dict:
            raise Exception(
                "app not found with id=<{0}> in={1}".format(find_app_id, str(self)))
        return self.app_dict[find_app_id]

    def cleanup(self):
        for app_id in self.app_dict:
            app = self.app_dict[app_id]
            self.logger.info("Clean app " + str(app))
            app.cleanup()

    def __str__(self):
        app_str_list = []
        for app_id in self.app_dict:
            app = self.app_dict[app_id]
            app_str_list += [str(app)]
        return "apps({})".format(str(app_str_list))
