import os
import re
import sys
import glob
import zipfile as zf
import datetime

filePath = "/home/FSICBC/liuhr/testRezip/"
##today = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
'''
def rezip(fileName):
    path,fileName = os.path.split(fileName)
    os.chdir(path) 
    if(zf.is_zipfile(fileName)):
        zipfile = zf.ZipFile(fileName,'r')
        newfileName = re.sub(r'\.\d{8}\.','.'+today+'.',fileName)
        newzipfile = zf.ZipFile(newfileName,'w',zf.ZIP_DEFLATED)
        for file in zipfile.namelist():
            try:
                zipfile.extract(file)
            except BaseException,e:
                print e.message
                sys.exit()
            newfile = re.sub(r'\.\d{8}\.','.'+today+'.',file)
            print file,"============>",newfile
            os.rename(file,newfile)
            newzipfile.write(newfile)
            os.unlink(newfile)   ## delete the extract file

        zipfile.close()
        newzipfile.close()
        os.unlink(fileName)  ## delete the original zip file    
    else:
        print "%s is not standard zip file,can not process ......" % (fileName)
'''
def rezip(fileName,today):
    path,fileName = os.path.split(fileName)
    os.chdir(path) 
    if(zf.is_zipfile(fileName)):
        zipfile = zf.ZipFile(fileName,'r')
        newfileName = re.sub(r'\.\d{8}\.','.'+today+'.',fileName)
        for file in zipfile.namelist():
            unzipCmd = "unzip "+fileName
            os.system(unzipCmd)
            newfile = re.sub(r'\.\d{8}\.','.'+today+'.',file)
            print file,"============>",newfile
            os.rename(file,newfile)
            zipCmd = "zip "+newfileName+" "+newfile
            os.system(zipCmd)
            os.unlink(newfile)   ## delete the extract file

        zipfile.close()
        os.unlink(fileName)  ## delete the original zip file    
    else:
        print "%s is not standard zip file,can not process ......" % (fileName)

def rename(fileName):
    path,fileName = os.path.split(fileName)
    os.chdir(path)
    newfileName = re.sub(r'\.\d{8}\.','.'+today+'.',fileName)
    print fileName,"===============>",newfileName
    os.rename(file,newfileName)



if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "python error: python rezipData.py [date]"
        sys.exit(1)
    fileList = glob.glob(filePath+'/*.zip')
    today = sys.argv[1]
    for fileName in fileList:
        rezip(fileName,today)
    ##fileList = glob.glob(filePath+'/*.txt')
    ##for fileName in fileList:
    ##    rename(fileName)


