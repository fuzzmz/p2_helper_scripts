import os
import optparse


def return_size(zipfile):
    v = ""
    try:
        v = v + str(os.path.getsize(zipfile))
    except WindowsError:
        sys.stderr.write(zipfile+" not found")
        sys.exit(1)
    return v


def replaceinfile(sizeoffile, inputfile, stringrplc):
    try:
        f = open(inputfile, "r")
    except IOError:
        sys.stderr.write(inputfile+" not found")
        sys.exit(1)
    contents = f.read()
    f.close()
    contents = contents.replace(stringrplc, sizeoffile)
    try:
        f = open(inputfile, "w")
    except IOError:
        sys.stderr.write(inputfile+" not found")
        sys.exit(1)

    f.write(contents)
    f.close()


def main():
    parser = optparse.OptionParser()
    parser.add_option('-i','--inputfile',
        dest = 'inputfile',
        action = 'store',
        help = 'input file to be replaced')
    parser.add_option('-z','--zipfile',
        dest = 'zipfile',
        action = 'store',
        help = 'zip file')
    parser.add_option('-s','--stringrplc',
        dest = 'stringrplc',
        action = 'store',
        help = 'string to replace')
    (opts, args) = parser.parse_args()
    inputfile = opts.inputfile
    zipfile = opts.zipfile
    stringrplc = opts.stringrplc
    sizeoffile = return_size(zipfile)
    replaceinfile(sizeoffile, inputfile, stringrplc)


if __name__ == '__main__':
    main()