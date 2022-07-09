from datetime import datetime, date

from flask import render_template, request, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


# USER SIDE URL

@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackVOList = feedbackDAO.userViewFeedback(feedbackVO)

            return render_template('user/addFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            feedbackFrom_LoginId = session['session_loginId']

            feedbackDate = date.today()

            now = datetime.now()
            feedbackTime = now.strftime("%H:%M:%S")

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))

        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)

@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackId = request.args.get('feedbackId')

            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


# Admin Side

@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':

            feedbackDAO = FeedbackDAO()
            adminfeedbackVOList = feedbackDAO.adminViewFeedback()

            return render_template('admin/viewFeedback.html', adminfeedbackVOList=adminfeedbackVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback', methods=['GET'])
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':

            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId

            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.adminReviewFeedback(feedbackVO)

            return redirect(url_for('adminViewFeedback'))

        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)
