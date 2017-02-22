import os
import sys
import datetime
import re
import ConfigParser as cp
import cx_Oracle as oracle

configFile = '/home/FSICBC/liuhr/exportData/export.cfg'
configList = []
oracleUser = 'fsicbc02'
oraclePass = 'FSICBC02'
oracleUrl = '172.17.0.120/orcl'
today = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")


def readConfig(config=None):
    print config
    if config:
        exportConfig = cp.SafeConfigParser()
        exportConfig.read(config)
        for section in exportConfig.sections():
            print section
            configDic = {}
            for option in exportConfig.options(section):
                print " ",option," = ",exportConfig.get(section,option)
                configDic[option] = exportConfig.get(section,option)
            configList.append(configDic)
    else:
        print "config file is not defined,exit program ......"
        sys.exit(1)


def exportData(cursor,exportInfo=None):
    if  exportInfo:
        path = exportInfo['path']
        fileName = exportInfo['filename']
        sql = exportInfo['sql']
        compress = exportInfo['compress']
        compressName = exportInfo['compressname']

        fileName = re.sub(r'\[YYYYMMDD\]',today,fileName)
        compressName = re.sub(r'\[YYYYMMDD\]',today,compressName)
        os.chdir(path)
        file = fileName
        compressFile = compressName
        with open(file,'w') as exp:
            cursor.execute(sql)
            resultSet = cursor.fetchall()
            for resultList in resultSet:
                result = '&&'.join(str(item) for item in resultList)
                result = result+'&&'+'\n'
                exp.write(result)

        if  compress:
            if compress == 'zip':
                zipCmd = 'zip '+compressFile+' '+file
                os.system(zipCmd)
                os.unlink(file)
        else:
            print "compress type is not defined ......"            
    else:
        print "export info is not defined,next ......"

if __name__ == '__main__':
    readConfig(configFile)
    connectUrl = oracleUser + '/' + oraclePass + '@' + oracleUrl
    db=oracle.connect(connectUrl)
    cursor = db.cursor()
    for dictInfo in configList:
        exportData(cursor,dictInfo)
    cursor.close()
    db.close()
        
    

