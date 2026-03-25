import re
import os
import yaml
from xffasttest.common import Dict
from xffasttest.utils.env import Env

class Utils:

    @staticmethod
    def traverse_dir(directory: str) -> list:
        test_files: list = []

        if os.path.isfile(directory):
            test_files.append(directory)
            return test_files

        for root, dirs, files in os.walk(directory):
            dirs.sort()
            files.sort()
            for file in files:

                if not file.endswith('.py') or file == '__init__.py':
                    continue 

                file_path = os.path.join(root, file)

                if os.path.isfile(file_path): 
                    test_files.append(file_path)
        return test_files

    @staticmethod
    def load_yaml(path) -> Dict:
        with open(path, "r", encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)

        pattern = r'\$\{(.*?)\}'
        def replace_env_vars(obj):
            if isinstance(obj, dict):
                return {k: replace_env_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_env_vars(element) for element in obj]
            elif isinstance(obj, str):
                match = re.match(pattern, obj)
                if match:
                    env_key = match.group(1)
                    value = Env.get_env(env_key, obj)
                    return value
                return obj
            else:
                return obj

        yaml_data = replace_env_vars(yaml_data)
        yaml_dict = Dict(yaml_data)
        return yaml_dict