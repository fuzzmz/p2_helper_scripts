import os
import zipfile
import subprocess
import sys
import xml.etree.ElementTree as ET
import shutil
from sys import platform as _platform

def unzip(componentToSign, dest_dir):
    with zipfile.ZipFile(componentToSign) as zf:
        zf.extractall(dest_dir)

def removeMD5(dest_dir):
    xmlpath = dest_dir+"/artifacts.xml"
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    for child in root:
        if child.tag.find('artifacts')>(-1):
            for anotherChild in child:
                if anotherChild.tag.find('artifact')>(-1):
                    for propertiesChild in anotherChild:
                        if propertiesChild.tag.find('properties')>(-1):
                            for propertyChild in propertiesChild:
                                if propertyChild.tag.find('property')>(-1):
                                    if propertyChild.attrib['name']=="download.md5":
                                        propertiesChild.remove(propertyChild)
                                        tree.write(xmlpath)

componentToSign = str(sys.argv[1])
workspace = str(sys.argv[2])
dest_dir = workspace+"/TempUnzip"
packageName = componentToSign
if os.path.exists (workspace+"\\TempUnzip"):
    shutil.rmtree(workspace+"\\TempUnzip")

if componentToSign[-3:]=="zip":
    unzip(componentToSign,dest_dir)
    if os.path.isfile(dest_dir+"/artifacts.xml"):
        removeMD5(dest_dir)
    elif os.path.isfile(dest_dir+"/artifacts.jar"):
        unzip(dest_dir+"/artifacts.jar",dest_dir)
        removeMD5(dest_dir)
        os.remove(dest_dir+"/artifacts.jar")
        if _platform == "win32" or _platform == "cygwin":
            subprocess.check_output(['wzzip', '-rp', '-yb', '-k', dest_dir+"/artifacts.jar", dest_dir+"/artifacts.xml"])
        elif _platform == "linux" or _platform == "linux2":
            # TODO do linux zip here
            subprocess.check_output(['zip', '-j', dest_dir+"/artifacts.jar", dest_dir+"/artifacts.xml"])
        else:
            print "Unknown platform"
        os.remove(dest_dir+"/artifacts.xml")
    os.remove(componentToSign)

    print "Success!!!"

else:
    print "Component must be of type '.zip' !!!"