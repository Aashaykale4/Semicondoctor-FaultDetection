
from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path: str) -> List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
        print(requirements)
        
    return requirements

setup(
    name="Faultdetection",
    version="0.1.0",
    install_requirments=('requirements.txt'),
    packages=find_packages()
)

