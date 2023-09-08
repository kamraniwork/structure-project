import os


class Configuration:
    DOCKER_SECRET_DEFAULT_LOCATION = "/run/secrets/"


    @classmethod
    def find_dotenv(cls, filename, alternative_env_search_dir):
        from dotenv import find_dotenv
        file_path = ""
        try:
            file_path = file_path = find_dotenv(filename=filename)
        except:
            print("Warning: First try to find .env file failed!")

        return file_path

    @classmethod
    def read_from_docker_secret(cls, attr_name: str):
        data = None
        try:
            with open(cls.DOCKER_SECRET_DEFAULT_LOCATION + attr_name, 'r') as file:
                data = file.read().rstrip()
        except:
            pass
        return data

    @classmethod
    def set_value_for_class(cls, clazz, attr_name, env_value: str, annotated_field_class=None):
        class_value = getattr(clazz, attr_name)
        if annotated_field_class and not type(annotated_field_class).__name__ == '_GenericAlias':
            if issubclass(annotated_field_class, str):
                return env_value
        if annotated_field_class:
            return eval(env_value)

        if class_value:
            if isinstance(class_value, str):
                return env_value
            return eval(env_value)
        return env_value
    @classmethod
    def configure(cls,cls_type: type, is_test=False,
                  alternative_env_search_dir: str = None, silent: bool = False):

        """
                Configure project specific configuration for commons lib
                @param cls_type:  Project specific configuration(e.g.  child of .. py:class::)
                @param is_test:
                @param alternative_env_search_dir:
        """
        if alternative_env_search_dir is None and not silent:
            print(
                "Warning: alternative_env_search_dir is set to None. .env files can not be found when venv dir located"
                "\noutside of project main directory. you can use alternative_env_search_dir=__file__ to avoid it."
                "\n use silent = True to suppress this warning")
        filename = '.env'
        if is_test:
            filename = '.env.test'

        from dotenv import load_dotenv, dotenv_values

        dotenv_values = dotenv_values(
            cls.find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir))
        for env_attr in dotenv_values:
            if not hasattr(cls_type, env_attr):
                # set .env field to class to replace with env values in next loop
                setattr(cls_type, env_attr, None)
        load_dotenv(cls.find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir))
        for attr_name in dir(cls_type):
            if attr_name.startswith("__") or callable(getattr(cls_type, attr_name)):
                continue

            read_value = cls.read_from_docker_secret(attr_name)

            if read_value is None:
                read_value = os.getenv(attr_name)
                if read_value is None:
                    continue
            try:
                final_value = cls.set_value_for_class(cls_type, attr_name, read_value)
                setattr(cls_type, attr_name, final_value)

            except:
                pass