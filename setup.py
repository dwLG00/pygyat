from setuptools import setup
from setuptools.command.build_py import build_py
from pygyat import VERSION_NUMBER
import shutil
from distutils.sysconfig import get_python_lib
import os
import pathlib

with open("README.md", "r") as fh:
    long_description = fh.read()

print('source loc: %s' % get_python_lib())

class build_py_with_pth_file(build_py):
    def run(self):
        super().run()

        python_lib = get_python_lib()
        dest_location = os.path.join(python_lib, 'pygyat.pth')
        source_location = './pygyat.pth'
        self.copy_file(source_location, dest_location, preserve_mode=0)

# Install python package, scripts and manual pages
setup(name="pygyat",
      version=VERSION_NUMBER,
      author="Shamith Pasula, Dylan Wallace",
      author_email="shamith09@berkeley.edu, dawallace2@wisc.edu",
      license="MIT",
      description="Python with rizz",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/dwLG00/pygyat",
      scripts=["scripts/gyat2py", "scripts/pygyat", "scripts/py2gyat"],
      data_files=[("man/man1", ["etc/pygyat.1", "etc/py2gyat.1", "etc/gyat2py.1"])],
      packages=["pygyat", "pygyat.codec"],
      cmd_class = {
          'build_py': build_py_with_pth_file,
      },
      zip_safe=False)

pth_path = pathlib.Path(__file__).parent / 'pygyat.pth'
dest_path = get_python_lib()
shutil.copy(pth_path, dest_path)
