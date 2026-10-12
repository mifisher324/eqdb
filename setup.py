from distutils.core import setup

setup(name='EQDB',
      version='2.1',
      description='EverQuest Database for EQ Emulator Server',
      install_requires=[
          'sqlalchemy',
          'flask',
          'mysqldb',
        ])
