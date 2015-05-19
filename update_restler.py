#! /usr/bin/env python
import sys
import os.path
import shutil

def main():
    restler_location = "../restler"
    
    if len(sys.argv) == 2:
        restler_location = sys.argv[1]
    elif len(sys.argv) > 2:
        print "usage: update_restler.py [path_to_restler_project]"
        sys.exit(-1)

    
    restler_module_dir = os.path.join(restler_location, 'restler')
    substrate_restler_module_dir = os.path.join("app", "lib", "substrate", "restler")

    if not os.path.exists(substrate_restler_module_dir):
        print "sanity check failure! restler module not found in substrate"
        sys.exit(-1)
    
    if os.path.exists(restler_module_dir) and os.path.isdir(restler_module_dir):
        shutil.rmtree(substrate_restler_module_dir)
        shutil.copytree(restler_module_dir, substrate_restler_module_dir)
    else:
        print "usage: update_restler.py [path_to_restler_project]\n"
        print "restler module not found in directory %s" % restler_location
        sys.exit(-1)        

if __name__ == '__main__':
    main()
