import os
import json

import dotenv
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def gen_agent() -> str:
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    return UserAgent(
        software_names=software_names,
        operating_systems=operating_systems,
        limit=100,
    ).get_random_user_agent()


def read_json(path) -> dict:
    with open(path, "r") as js:
        json_to_dict = json.load(js)
    return json_to_dict

def read_dotenv(path) -> dict:
    dotenv.load_dotenv(dotenv.find_dotenv('./config/db.env'))


def check_dir(path: str) -> None:
    if path is None:
        return
    if not os.path.exists(path):
        os.mkdir(path)



