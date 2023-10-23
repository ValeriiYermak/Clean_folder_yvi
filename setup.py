from setuptools import setup, find_namespace_packages



setup(
    name='Clean_folder_yvi',
    version='0.0.1',
    description='File Sorter',
    author='Yermak Valerii',
    author_email='yermakvaleriy@gmail.com',
    license='MIT',
    classifiers = ["Programming Language :: Python :: 3", 
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",],
    packages=find_namespace_packages(),
    entry_points={'console_scripts':['clean=Clean_folder_yvi.clean:start']},
)