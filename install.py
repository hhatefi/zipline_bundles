import argparse
import logging
import sys, os
import shutil

### configure logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# check if zipline is installed
try:
    import zipline.data.bundles as bld
except ImportError:
    logging.error('cannot found zipline. Run the installer in an environment where zipline is installed.')
    sys.exit(1)

### initialize the input argument parser
parser=argparse.ArgumentParser(description='Add zipline bundles')
parser.add_argument('-f', '--force', action='store_true')

### parse input arguments
input_args=parser.parse_args()

### source files and directory
src_dir=os.path.join(os.getcwd(), 'lib')
src_ext=['extension.py']
src_ing=['ingester.py', 'iex.py', 'yahoo.py', 'binance.py']

### destination directories
dst_ext=os.path.join(os.path.expanduser('~'), '.zipline')
# check the existence of zipline home
if not os.path.isdir(dst_ext):
    logging.error("zipline home ('{}') does not exist.")
    sys.exit(1)

dst_ing=bld.__path__[0]


def copy(filelist, dest, src):
    for f in filelist:
        dstf=os.path.join(dest, f)
        if not input_args.force and os.path.exists(dstf):
            logging.error("'{}' already exists.".format(dstf))
            sys.exit(1)
        else:
            srcf=os.path.join(src, f)
            logging.info("copying '{}' to '{}'".format(srcf, dest))
            try:
                shutil.copyfile(srcf, dstf)
            except Exception as exp:
                loggin.error("error while copying '{}' to '{}': {}".format(srcf, dest, exp))
                sys.exit(1)

copy(src_ext, dst_ext, src_dir)
copy(src_ing, dst_ing, src_dir)
