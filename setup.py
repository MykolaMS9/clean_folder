from setuptools import setup

setup(
    name='Clean_Folder',
    version='0.0.1',
    description='Clean special folder in your PC',
    author='MykolaMS9',
    author_email='some_email@gmail.com',
    url='https://github.com/MykolaMS9',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3'],
    packages=['clean_folder'],
    include_package_data=True,
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:run']}
)