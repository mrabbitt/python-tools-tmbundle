import os.path
import site

lib_dir = os.path.dirname(os.path.realpath(__file__))
site.addsitedir(lib_dir)
