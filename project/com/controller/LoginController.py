from flask import request, render_template, redirect, session, url_for

from project import app
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.PredictionDAO import PredictionDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PredictionVO import PredictionVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/', methods=['GET'])
def adminLaodLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/validateLogin', methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        lenloginDictList = len(loginDictList)

        if lenloginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == 'Inactive':
            msg = 'Your account is blocked by admin.'

            return render_template('admin/login.html', error=msg)


        else:

            for row in loginDictList:

                loginId = row['loginId']

                loginUsername = row['loginUsername']

                loginRole = row['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashbord', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewUser()

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            totalComplainList = complainDAO.adminViewComplain()
            totalComplainCount = len(totalComplainList)

            complainVO.complainStatus = "Pending"
            totalPendingComplainList = complainDAO.adminTotalPendingComplain(complainVO)
            totalPendingComplainCount = len(totalPendingComplainList)

            feedbackDAO = FeedbackDAO()
            totalFeedbackList = feedbackDAO.adminViewFeedback()
            totalFeedbackCount = len(totalFeedbackList)

            return render_template('admin/index.html', registerVOList=registerVOList,
                                   totalComplainCount=totalComplainCount,
                                   totalFeedbackCount=totalFeedbackCount,
                                   pendingComplainCount=totalPendingComplainCount)
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashbord', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainFrom_LoginId = session['session_loginId']
            totalComplainList = complainDAO.userViewComplain(complainVO)
            totalComplainCount = len(totalComplainList)

            complainVO.complainStatus = "Pending"
            totalPendingComplainList = complainDAO.userTotalPendingComplain(complainVO)
            totalPendingComplainCount = len(totalPendingComplainList)

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']
            totalFeedbackList = feedbackDAO.userViewFeedback(feedbackVO)
            totalFeedbackCount = len(totalFeedbackList)

            register_LoginId = session['session_loginId']
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerVO.register_LoginId = register_LoginId
            registerVOList = registerDAO.registerDetailByLoginId(registerVO)

            prediction_RegisterId = registerVOList[0].registerId

            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()
            predictionVO.prediction_RegisterId = prediction_RegisterId
            predictionVOList = predictionDAO.viewPredictionCrops(predictionVO)

            return render_template('user/index.html', predictionVOList=predictionVOList,
                                   totalComplainCount=totalComplainCount,
                                   pendingComplainCount=totalPendingComplainCount,
                                   totalFeedbackCount=totalFeedbackCount)
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:
            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'user':

                return 'user'
        else:
            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect('/')
    except Exception as ex:
        print(ex)
