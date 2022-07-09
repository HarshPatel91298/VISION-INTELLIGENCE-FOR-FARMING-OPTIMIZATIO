import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CityDAO import CityDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.StateDAO import StateDAO
from project.com.dao.UserDAO import UserDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route("/user/newPassword", methods=['GET'])
def userNewPassword():
    try:
        return render_template('user/forgotPassword.html')
    except Exception as ex:
        print(ex)


@app.route("/user/forgotPassword", methods=['POST'])
def userForgotPassword():
    try:

        loginUsername = request.form['loginUsername']
        session['loginUsername'] = loginUsername

        loginVO = LoginVO()

        userDAO = UserDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginRole = "user"

        userVOList = userDAO.validateUser(loginVO)

        userDictList = [i.as_dict() for i in userVOList]

        lenloginDictList = len(userDictList)

        if lenloginDictList == 0:
            msg = 'Username not registered with us!'

            return render_template('user/forgotPassword.html', error=msg)

        elif userDictList[0]['loginStatus'] == 'Inactive':  # check user active or not

            msg = 'Your account blocked by admin.'

            return render_template('user/forgotPassword.html', error=msg)

        else:

            # send new password on Username

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            sender = "cropdetection2020@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "CROP DETECTION PASSWORD"

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "viffo@2020")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            # set Username and password in loginVO object
            loginVO.loginUsername = loginUsername
            loginVO.loginPassword = loginPassword

            userDAO.updatePassword(loginVO)

            server.quit()

            return redirect(url_for('adminLaodLogin'))


    except Exception as ex:
        print(ex)


@app.route('/user/changePassword', methods=['GET'])
def userChangePassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/editPassword.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/updatePassword', methods=['POST'])
def userUpdatePassword():
    try:
        if adminLoginSession() == 'user':
            loginId = session['session_loginId']

            oldpassword = request.form['oldpassword']
            newpassword = request.form['newpassword']
            confirmpassword = request.form['confirmpassword']

            loginVO = LoginVO()
            userDAO = UserDAO()

            loginVO.loginId = loginId
            userList = userDAO.chagePassword(loginVO)

            if userList.loginPassword == oldpassword:

                if newpassword == oldpassword:

                    msg = 'Current Password and New Password Shoud be different.'
                    return render_template('user/editPassword.html', error=msg)

                elif newpassword == confirmpassword:

                    loginVO.loginPassword = newpassword
                    userDAO.chagePassword(loginVO)

                else:

                    msg = 'Password does not match!'
                    return render_template('user/editPassword.html', error=msg)
            else:

                msg = 'CurrentPassword is Wrong!'

                return render_template('user/editPassword.html', error=msg)

            msg = 'Password Change Successfully.'

            return render_template('user/editPassword.html', msg=msg)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/user/editRegister', methods=['GET'])
def userEditRegister():
    try:
        if adminLoginSession() == 'user':
            stateDAO = StateDAO()
            stateVOList = stateDAO.viewState()

            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            loginId = session['session_loginId']

            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerVO.register_LoginId = loginId

            registerVOList = registerDAO.editProfile(registerVO)

            return render_template('user/editProfile.html', registerVOList=registerVOList, stateVOList=stateVOList,
                                   cityVOList=cityVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/updateRegister', methods=['POST'])
def userUpdateRegister():
    try:
        if adminLoginSession() == 'user':
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            loginId = request.form['loginId']
            loginUsername = request.form['loginUsername']

            registerId = request.form['registerId']
            registerCompanyname = request.form['registerCompanyname']
            register_StateId = request.form['register_StateId']
            register_CityId = request.form['register_CityId']
            registerAddress = request.form['registerAddress']
            registerContactNumber = request.form['registerContactNumber']

            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = loginId
            loginList = loginDAO.viewLogin(loginVO)


            if loginList[0].loginUsername == loginUsername:
                pass
            else:
                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                sender = "cropdetection2020@gmail.com"

                receiver = loginUsername

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "ACCOUNT PASSWORD"

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "VISION INTELLIGENCE FOR FARMING OPTIMIZATION@2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword

                loginDAO.updateLogin(loginVO)

            registerVO.registerId = registerId
            registerVO.registerCompanyname = registerCompanyname
            registerVO.register_StateId = register_StateId
            registerVO.register_CityId = register_CityId
            registerVO.registerAddress = registerAddress
            registerVO.registerContactNumber = registerContactNumber

            registerDAO.updateRegister(registerVO)
            return redirect(url_for('userLoadDashboard'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
