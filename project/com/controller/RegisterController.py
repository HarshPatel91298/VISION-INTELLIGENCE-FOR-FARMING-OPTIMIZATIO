import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for, jsonify

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.CityDAO import CityDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.StateDAO import StateDAO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister', methods=['GET'])
def userLoadRegister():
    try:

        stateDAO = StateDAO()
        stateVOList = stateDAO.viewState()

        cityDAO = CityDAO()
        cityVOList = cityDAO.viewCity()

        return render_template('user/register.html', stateVOList=stateVOList, cityVOList=cityVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        imageDAO = ImageDAO()
        cityVO = CityVO()

        loginUsername = request.form['loginUsername']

        registerCompanyname = request.form['registerCompanyname']
        register_StateId = request.form['register_StateId']

        cityName = request.form['register_CityId']


        cityVO.cityName = cityName
        cityVOList = imageDAO.viewCityByCityName(cityVO)
        register_CityId = cityVOList[0].cityId

        registerAddress = request.form['registerAddress']
        registerContactNumber = request.form['registerContactNumber']

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

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)



        registerVO.register_LoginId = loginVO.loginId
        registerVO.registerCompanyname = registerCompanyname
        registerVO.register_StateId = register_StateId
        registerVO.register_CityId = register_CityId

        registerVO.registerAddress = registerAddress
        registerVO.registerContactNumber = registerContactNumber

        registerDAO.insertregister(registerVO)

        server.quit()

        return redirect('/')

    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            userVOList = registerDAO.viewUser()

            return render_template('admin/viewUser.html', userVOList=userVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginId = request.args.get('loginId')
            loginVO = LoginVO()
            registerDAO = RegisterDAO()

            loginVO.loginId = loginId
            loginVO.loginStatus = "Inactive"

            registerDAO.updateUserStatus(loginVO)
            return redirect(url_for('adminViewUser'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['GET'])
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginId = request.args.get('loginId')
            loginVO = LoginVO()
            registerDAO = RegisterDAO()

            loginVO.loginId = loginId
            loginVO.loginStatus = "active"

            registerDAO.updateUserStatus(loginVO)

            return redirect(url_for('adminViewUser'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadCityByStateRegister')
def adminAjaxCityDataRegister():
    try:
        cityVO = CityVO()
        cityDAO = CityDAO()

        city_StateId = request.args.get('image_StateId')
        cityVO.city_StateId = city_StateId

        ajaxCropVOList = cityDAO.viewCityDetailsByState(cityVO)

        adminAjaxCityVOList = []
        for i in ajaxCropVOList:
            adminAjaxCityVOList.append(i)

        return jsonify(adminAjaxCityVOList)

    except Exception as ex:
        print(ex)
