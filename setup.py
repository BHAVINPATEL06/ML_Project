from setuptools import find_packages,setup
from typing import List

### THis '-e .' will be there in the requirements.txt it's mapping with this setup.py
HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    '''
        This Function will return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

        return requirements

setup(
    name='mlproject',
    version='0.0.1',
    author='Bhavin',
    author_email='bhavinpatel242846@gmail.com',
    packages=find_packages(),
    install_requries = get_requirements('requirements.txt')
)