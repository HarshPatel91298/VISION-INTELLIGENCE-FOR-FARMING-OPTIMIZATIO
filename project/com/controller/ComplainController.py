import os,imghdr
import smtplib
from datetime import datetime, date
from secrets import token_urlsafe

from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


# User Side URL
@app.route('/user/loadComplain', methods=['GET'])
def userLoadComplain():
    try:
        if adminLoginSession() == 'user':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainFrom_LoginId = session['session_loginId']
            complainVO.complainStatus = "Replied"
            userComplainVOList = complainDAO.userViewComplain(complainVO)

            return render_template('user/addComplain.html',userComplainVOList = userComplainVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            UPLOAD_FOLDER = 'project/static/adminResources/complainAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainTokenId = token_urlsafe(10)

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            file = request.files['file']
            complainFrom_LoginId = session['session_loginId']

            now = datetime.now()
            complainDate = date.today()
            complainTime = now.strftime("%H:%M:%S")

            complainFileName = secure_filename(file.filename)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainTokenId = complainTokenId
            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = "Pending"
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace("project", "..")
            complainVO.complainFrom_LoginId = complainFrom_LoginId

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userLoadComplain'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['GET'])
def userViewComplain():
    try:
        if adminLoginSession() == 'user':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainFrom_LoginId = session['session_loginId']
            userComplainVOList = complainDAO.userViewComplain(complainVO)

            return render_template('user/viewComplain.html', userComplainVOList=userComplainVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainId = request.args.get('complainId')
            complainList = complainDAO.deleteComplain(complainVO)

            # Delete user Complain file
            complainFilePath = complainList.complainFilePath.replace("..", "project") + complainList.complainFileName
            os.remove(complainFilePath)

            if complainList.complainTo_LoginId is not None:  # Delete admin replied file
                replyFilePath = complainList.replyFilePath.replace("..", "project") + complainList.replyFileName
                os.remove(replyFilePath)

            return redirect(url_for('userLoadComplain'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['GET'])
def userViewComplainReply():
    try:
        if adminLoginSession() == 'user':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainId = request.args.get('complainId')
            complainReplyVOList = complainDAO.viewComplainReply(complainVO)

            return render_template('user/viewComplainReply.html', complainReplyVOList=complainReplyVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


# Admin side


@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':

            complainDAO = ComplainDAO()

            adminComplainVOList = complainDAO.adminViewComplain()
            return render_template('admin/viewComplain.html', adminComplainVOList=adminComplainVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':

            complainId = request.args.get('complainId')

            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:

        if adminLoginSession() == 'admin':

            UPLOAD_FOLDER = 'project/static/adminResources/replyComplainAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            complainTo_LoginId = session['session_loginId']

            replyDate = date.today()

            now = datetime.now()
            replyTime = now.strftime("%H:%M:%S")

            file = request.files['file']
            replyFileName = secure_filename(file.filename)
            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainStatus = "Replied"
            complainVO.complainTo_LoginId = complainTo_LoginId


            complainDAO.insertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))

        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/viewComplainReply', methods=['GET'])
def adminViewComplainReply():
    try:
        if adminLoginSession() == 'admin':

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainId = request.args.get('complainId')
            complainReplyVOList = complainDAO.viewComplainReply(complainVO)

            return render_template('admin/viewComplainReply.html', complainReplyVOList=complainReplyVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)
