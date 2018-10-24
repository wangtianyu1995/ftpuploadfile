# coding=utf-8
import socket
import string
import os
import time
import datetime
import shutil
import zipfile
from ftplib import FTP
import ftplib
import json
import codecs,sys
import configparser
#import  win32api
import logging.handlers
from logging.handlers import RotatingFileHandler

##########################
FileNotFounderror_return=0
##########################

def Zip(zipname):
    try:
        z = zipfile.ZipFile('%s' % zipname, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(temppath):
            for filename in filenames:
                z.write(os.path.join(dirpath, filename))
                print('Zip ing!!!')

    except ftplib.all_errors as e:
        zipstrerror = '"%s"' % e
        sendziperror='{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(cmd='{"cmd": "OnLogUploadState"',percent='"percent":"0"',
                                                                                            totalsize='"totalsize":"0"',
                                                                                            phase='"phase": "upload"',errorcode='"errorcode":"-3"',
                                                                                            description='"description":'+zipstrerror+'}')
        ziperror_tobridge=sendziperror.encode('utf-8')
        time.sleep(0.01)
        #s1.send(ziperror_tobridge)
        logging.warning('zip failed'+str(e))
        print('zip failed'+str(e))
        ftp.quit()


#######################################################################################################################

uploadprogress = 0
def UpLoadLog():
    nowtime=time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    filename = "%s"%nowtime+zipname

    try:
        starttime=datetime.datetime.now()
        ftp.storbinary('STOR %s' % filename, open(zipname, 'rb'),10000000,storCallback)
        print('ftpuploadlog 100%')

    except ftplib.all_errors as e:
        ftpuploadlogstrerror='"%s"'%e
        sendjsonfailstrtobridge ='{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(cmd='{"cmd": "OnLogUploadState"',percent='"percent":"0"',
                                                                                            totalsize='"totalsize":"0"',
                                                                                            phase='"phase": "upload"',errorcode='"errorcode":"-2"',
                                                                                            description='"description":'+ftpuploadlogstrerror+'}')
        errorcode_tobridge = sendjsonfailstrtobridge.encode("utf-8")

        #s1.send(errorcode_tobridge)

        endtime = datetime.datetime.now()
        if (endtime - starttime)>datetime.timedelta(seconds=6)or\
                (endtime - starttime) <datetime.timedelta(seconds=4):
            logging.warning('ftp upload failed' + str(e))
            print('ftp upload failed' + str(e))

            ftp.quit()

    except AttributeError as aError:
        ftpconnecerror = '"%s"' % aError
        ftpconnecerrortobridge = '{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(
            cmd='{"cmd": "OnLogUploadState"', percent='"percent":"0"',
            totalsize='"totalsize":"0"',
            phase='"phase": "upload"', errorcode='"errorcode":"-5"',
            description='"description":' + ftpconnecerror + '}')
        ftpconnecerror_tobridge = ftpconnecerrortobridge.encode("utf-8")

        #s1.send(ftpconnecerror_tobridge)
        logging.warning('ftpconnecerror' + str(aError))
        print('ftpconnecerror' + str(aError))
        ftp.quit()
    #ftp.retrbinary("RETR %s"%filename,open('./My.zip','wb').write)

######################
def storCallback(a):
    filesize=os.stat("./%s"%zipname).st_size

    #everyfileuloadsize = '%.2f%%' % ((len(a) / filesize) * 100)
    global uploadprogress
    uploadprogress+=len(a)

    sendstr = '"%d"' % len(a)

    sendstr2 = '"%.2f%%"' % ((uploadprogress / filesize) * 100)

    sendjsontobridge='{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(cmd='{"cmd": "OnLogUploadState"',percent='"percent":'+sendstr2,
                                                                                            totalsize='"totalsize":'+sendstr,
                                                                                            phase='"phase": "upload"',errorcode='"errorcode": "0"',
                                                                                            description='"description": "0_is_uploadlog_success"}')

    print(sendjsontobridge,type(sendjsontobridge))

    OnLogUploadState_tobridge=sendjsontobridge.encode("utf-8")
    time.sleep(0.01)
    #s1.send(OnLogUploadState_tobridge)
    logging.warning(sendjsontobridge)
    print(OnLogUploadState_tobridge)
######################################

def CopyTree(dir):

    if os.path.exists('./4Gyaobao') == False:
        os.mkdir("./4Gyaobao")

    if os.path.exists('./4Gyaobao/assembler') == False:
        os.mkdir("./4Gyaobao/assembler")
    if os.path.exists('./4Gyaobao/autogate') == False:
        os.mkdir("./4Gyaobao/autogate")
    if os.path.exists('./4Gyaobao/DetectClient') == False:
        os.mkdir("./4Gyaobao/DetectClient")
    if os.path.exists('./4Gyaobao/webservice') == False:
        os.mkdir("./4Gyaobao/webservice")
    if os.path.exists('./4Gyaobao/pppd') == False:
        os.mkdir("./4Gyaobao/pppd")

    try:
        for i in range(len(dir)):
            for dirpath, dirnames, filenames in os.walk(dir[i]):
                for filename in filenames:
                    statinfo = os.stat(os.path.join(dirpath, filename))
                    a = statinfo.st_ctime
                    begin_local_time = datetime.datetime.fromtimestamp(int(a))
                    now = datetime.datetime.now()
                    timedifferent = now - begin_local_time

                    if (timedifferent < datetime.timedelta(days=7)):
                            if i==0:
                                shutil.copyfile(os.path.join(dirpath, filename), './4Gyaobao/assembler/%s' % filename)
                            if i==1:
                                shutil.copyfile(os.path.join(dirpath, filename), './4Gyaobao/autogate/%s' % filename)
                            if i==2:
                                shutil.copyfile(os.path.join(dirpath, filename), './4Gyaobao/DetectClient/%s' % filename)
                            if i==3:
                                shutil.copyfile(os.path.join(dirpath, filename), './4Gyaobao/webservice/%s' % filename)
                            if i==4:
                                shutil.copyfile(os.path.join(dirpath, filename), './4Gyaobao/pppd/%s' % filename)

    except FileNotFoundError as e:
        global FileNotFounderror_return
        FileNotFounderror_return=1
        FileNotFounderror = '"%s"' % e
        sendFileNotFounderrortobridge = '{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(
            cmd='{"cmd": "OnLogUploadState"', percent='"percent":"0"',
            totalsize='"totalsize":"0"',
            phase='"phase": "upload"', errorcode='"errorcode":"-4"',
            description='"description":' + FileNotFounderror + '}')
        FileNotFounderror_tobridge = sendFileNotFounderrortobridge.encode("utf-8")

        #s1.send(FileNotFounderror_tobridge)
        logging.warning('FileNotFound failed' + str(e))
        print('FileNotFound failed' + str(e))


######################
def RotatingFile():
    if os.path.exists('./LOG') == False:
        os.mkdir("./LOG")
    Rthandler = RotatingFileHandler('LOG//myftp.log', maxBytes=2*1024*1024,backupCount=5)
    Rthandler.setLevel(logging.WARN)

    log_fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(log_fmt)
    Rthandler.setFormatter(formatter)

    logging.getLogger('').addHandler(Rthandler)

######################
def FtpConnect():
    ftpurl=cp.get("url","ftpurl")
    ip = '%s'%ftpurl
    ftpuser=cp.get("ftpuser","user")
    user='%s'%ftpuser
    ftppassword=cp.get("ftppassword","password")
    password ='%s'%ftppassword
    ftpcwd=cp.get("ftpcwd","cwd")
    cwd='%s'%ftpcwd

    try:
        ftp.connect(ip,timeout=10)
        ftp.login(user, password)
        # print(ftp.getwelcome())
        ftp.cwd(cwd)

    except OSError as oe:
        Netconnecterror = '"%s"' % oe
        oeerror = '"%s"' %oe.args[0]
        sendNetconnecterror = '{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(
            cmd='{"cmd": "OnLogUploadState"', percent='"percent":"0"',
            totalsize='"totalsize":"0"',
            phase='"phase": "upload"', errorcode='"errorcode":' + oeerror,
            description='"description":' + Netconnecterror + '}')
        sendNetconnecterror_tobridge = sendNetconnecterror.encode('utf-8')

        #s1.send(sendNetconnecterror_tobridge)
        logging.warning('Net connect failed' + str(oe))
        print('Net connect failed' + str(oe))
        print(sendNetconnecterror_tobridge)
        ftp.quit()
    except ftplib.all_errors as e:
        connectstrerror='"%s"'%e
        sendftpconnecterror = '{cmd},{percent},{totalsize},{phase},{errorcode},{description}'.format(
            cmd='{"cmd": "OnLogUploadState"', percent='"percent":"0"',
            totalsize='"totalsize":"0"',
            phase='"phase": "upload"', errorcode='"errorcode":"-1"' ,
            description='"description":'+ connectstrerror+'}')
        sendftpconnecterror_tobridge=sendftpconnecterror.encode('utf-8')

        #s1.send(sendftpconnecterror_tobridge)
        logging.warning('connect failed'+str(e))
        print('connect failed'+str(e))
        ftp.quit()


if __name__=="__main__":

    RotatingFile()
    ##################
    print('come in FtpUpLoadLog success!!!!')

    sysargv=sys.argv
    #uuidJsonstr=s1.recv()
    uuid=sysargv[1]
    #procdurename=sysargv[2]
    #print(sysargv[1],type(sysargv[1]),sysargv[2],type(sysargv[2]))
    ###################

    cp=configparser.ConfigParser()
    cp.read("./uploadset.cfg",encoding='utf-8')

    pathcode=cp.get("path","assembler")
    pathcode2=cp.get("path","autogate")
    pathcode3=cp.get("path","DetectClient")
    pathcode4=cp.get("path","webservice")
    pathcode5=cp.get("path","pppd")

    logging.warning('%s'%pathcode)
    logging.warning('%s'%pathcode2)
    logging.warning('%s'%pathcode3)
    logging.warning('%s'%pathcode4)
    logging.warning('%s'%pathcode5)

   # temppath=win32api.GetTempPath()

    temppath='./4Gyaobao'
    shutil.rmtree('./4Gyaobao',True)

    ##############################
    listdir = []
    listdir.append(pathcode)
    listdir.append(pathcode2)
    listdir.append(pathcode3)
    listdir.append(pathcode4)
    listdir.append(pathcode5)
    dir = listdir
    CopyTree(dir)

    #global FileNotFounderror_return
    if FileNotFounderror_return == 0:

        ############################
        time.sleep(1)

        zipname='Yaobao'+'UpLoadLog'+uuid+'.zip'
        ###########################
        ftp = FTP(timeout=30)

        ftp.set_debuglevel(0)
        #########################
        FtpConnect()
        #########################
        Zip(zipname)
        UpLoadLog()













