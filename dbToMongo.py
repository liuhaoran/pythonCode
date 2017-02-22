#!/usr/bin/python

#coding=utf-8

import cx_Oracle
import sys
import urllib
import os
from pymongo import MongoClient

def connectDB(usr,passwd,url):
    connstr=usr+'/'+passwd+'@'+url
    db=cx_Oracle.connect(connstr)
    return db

def sqlSelect(sql,db):
    cr=db.cursor()
    cr.execute(sql)
    rs=cr.fetchall()
    cr.close()
    return rs

def mongoInsert(mongodb,cpCode,saveData):
    if len(saveData)>0:
        mongoTemp='tb_user_mkt_page_order_'+cpCode+'_temp'
        print mongoTemp
        mongodb[mongoTemp].drop()
        result = mongodb[mongoTemp].insert_many(saveData)
        print result.inserted_ids
        return len(result.inserted_ids)
    else:
        print '%s have not data in tb_user_mkt_page_order'%cpCode
        return 0

def mongoRename(mongodb,cpCode):
    mongoCol='tb_user_mkt_page_order_'+cpCode
    mongoTemp=mongoCol+'_temp'
    mongoBak=mongoCol+'_bak'
    mongodb[mongoBak].drop()
    mongodb[mongoCol].rename(mongoBak)
    mongodb[mongoTemp].rename(mongoCol)



if __name__=='__main__':
    os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
    usr='fsicbc02'
    passwd='FSICBC02'
    url='172.17.0.120/orcl'

    mongoUrl='mongodb://172.17.0.120:27017,172.17.0.121:27017,172.17.0.122:27017/repliaSet=rs01'
    ##mongoIp='172.17.0.120'
    ##mongoPort=27017
    
    =MongoClient(mongoUrl)
    mongodb=mongoclient.icbc
    	
    db=connectDB(usr,passwd,url)
    sql='select vc_cp_code from tb_cpm_detail where vc_cp_status=\'1\''
    rs=sqlSelect(sql,db)
    for cpCode in rs:    
        sql='select vc_user_nbr,vc_camp_id,nb_order from tb_user_mkt_page_order where \
        vc_camp_id in (select vc_camp_id from tb_cap_page_contact where vc_contact_id=\''+cpCode[0]+'\')'
        rs2=sqlSelect(sql,db)
        saveData=[]
        for pageOrder in rs2:
            print pageOrder
            saveData.append({'mobileno':pageOrder[0],'pageid':pageOrder[1],'order':pageOrder[2]})

        count=mongoInsert(mongodb,cpCode[0],saveData)
        print count
        print 'rename mongodb'+cpCode[0] 
        if count>0:
            mongoRename(mongodb,cpCode[0])
        else:
            print cpCode[0]+'insert Mongo unsucessfully or no data insert'       

    db.close()  
