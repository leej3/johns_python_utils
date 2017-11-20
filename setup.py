from setuptools import setup

setup(name='johns_python_utils',
      version='0.1',
      description="some helper functions",
      url="https://github.com/leej3/johns_python_utils.git",
      author='John Lee',
      author_email='johnleenimh@gmail.com',
      license='MIT',
      packages=['johns_python_utils'],
      install_requires=[
          'pathlib',
          'sklearn',
          'pandas',
      ],
      zip_safe=False)
