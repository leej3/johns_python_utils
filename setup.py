from setuptools import setup

setup(name='johns_hpc_helpers',
      version='0.1',
      description='Some redundant scripts. Some very helpful scripts...',
      url='http://github.com/johns_hpc_scripts',
      author='John Lee',
      author_email='johnleenimh@gmail.com',
      license='MIT',
      packages=['johns_hpc_helpers'],
      install_requires=[
          'pathlib',
          'sklearn',
          'pandas',
      ],
      zip_safe=False)
