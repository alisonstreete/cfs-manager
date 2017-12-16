from setuptools import setup

def readme():
    with open('./docs/README.rst') as f:
        return f.read()

setup(name="CFS_Manager",
    version='1.3.0',
    description="A virtual filesystem for accessing storage on multiple cloud services.",
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Environment :: Console',
        'Topic :: System :: Archiving :: Mirroring',
        'Intended Audience :: End Users/Desktop',
        ],
    url='https://github.com/alisonstreete/cfs-manager',
    author='Alison Streete',
    author_email='alison.streete@gmail.com',
    license='Apache License 2.0',
    packages=['cfs_manager'],
    install_requires=[
        'dropbox>=8.5',
        'pcloud==1.0a4',
        'pydrive>=1.3',
        'boxsdk>=1.5,<2.0'
        ],
    entry_points='''
      [console_scripts]
      cfs_manager=cfs_manager.cli:loop
      cfs-manager=cfs_manager.cli:loop
      cfsm=cfs_manager.cli:loop
      cfs-do=cfs_manager.cli:once
      cfs-watch=cfs_manager.cfs_watcher:main
      cfs-config=cfs_manager.configuration:main
    ''',
    include_package_data=True,
    zip_safe=False)