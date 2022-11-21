from setuptools import setup

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setup(
    name='',
    version='0.0.1',
    description='',
    url='https://github.com/nda111/ConfigYaml',
    author='Yu Geunhyeok',
    author_email='geunhyeok0111@gmail.com',
    license='MIT License',
    packages=['cfgyaml'],
    zip_safe=False,
    install_requires=requirements,
)
