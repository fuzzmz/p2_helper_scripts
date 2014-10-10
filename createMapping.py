import os
import optparse


def parseMap(file):
    map = open(file)
    strLN = ""
    for line in map:
        source=line.split(',')[1].rstrip()
        linkFull=line.split(',')[0]
        locstart=linkFull.rindex('/')
        path=linkFull[0:locstart+1].rstrip()
        link=linkFull[locstart+1:].rstrip()
        strLN+="    ln(targetDir:${installFolder}/." + path + ",linkTarget:" + source + ",linkName:" + link +");\\\n"
        os.remove(linkFull)
    pathCHMOD = path.split('/')[1].rstrip()
    strLoc = "    chmod(targetDir:${installFolder}/../,targetFile:" + pathCHMOD + ",options:-R,permissions:777);\\\n    chmod(targetDir:${installFolder}/../,targetFile:" + pathCHMOD + ",options:-R,permissions:+x);"
    strReplace = strLN + strLoc
    return strReplace


def updateP2(strReplace, p2):
    p2file = open(p2, "r")
    s = p2file.read()
    p2file.close()
    s = s.replace(":true);", ":true);\\\n" + strReplace)
    p2file = open(p2, "w")
    p2file.write(s)
    p2file.close()


def main():
    parser = optparse.OptionParser()

    parser.add_option('-p', '--path',
                      dest='path',
                      action='store',
                      help='path to p2inf')

    (opts, args) = parser.parse_args()
    p2 = opts.path

    strReplace = parseMap("map.txt")
    updateP2(strReplace, p2)


if __name__ == '__main__':
    main()