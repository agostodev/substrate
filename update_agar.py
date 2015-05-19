#! /usr/bin/env python
import sys
import os.path
import shutil

def main():
    agar_location = "../agar"
    
    if len(sys.argv) == 2:
        agar_location = sys.argv[1]
    elif len(sys.argv) > 2:
        print "usage: update_agar.py [path_to_agar_project]"
        sys.exit(-1)

    
    agar_module_dir = os.path.join(agar_location, 'agar')
    substrate_agar_module_dir = os.path.join("app", "lib", "substrate", "agar")

    if not os.path.exists(substrate_agar_module_dir):
        print "sanity check failure! agar module not found in substrate"
        sys.exit(-1)
    
    if os.path.exists(agar_module_dir) and os.path.isdir(agar_module_dir):
        shutil.rmtree(substrate_agar_module_dir)
        shutil.copytree(agar_module_dir, substrate_agar_module_dir)
    else:
        print "usage: update_agar.py [path_to_agar_project]\n"
        print "agar module not found in directory %s" % agar_location
        sys.exit(-1)        

if __name__ == '__main__':
    main()
