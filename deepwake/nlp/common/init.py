import yaml
from deepwake.nlp.common.constant import CONFIG_PATH
from deepwake.nlp.common.utils import get_absolute_path
import os
path = os.getcwd()
print(path)
with open(get_absolute_path(CONFIG_PATH), 'r') as reader:
    CONFIG = yaml.load(reader)