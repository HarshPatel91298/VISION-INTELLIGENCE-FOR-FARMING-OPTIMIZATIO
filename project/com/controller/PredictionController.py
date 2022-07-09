from flask import request, render_template, redirect, url_for, session, jsonify, json

from project import app
from datetime import date
import time
from project.com.controller.CropPrice_YieldPrediction import CropPrice_YieldPrediction
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CityDAO import CityDAO
from project.com.dao.CropRatioDAO import CropRatioDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.PredictionDAO import PredictionDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.CityVO import CityVO
from project.com.vo.CropRatioVO import CropRatioVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.PredictionVO import PredictionVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadPrediction', methods=['GET'])
def userLoadPrediction():
    try:
        if adminLoginSession() == 'user':
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCityDetails()

            cropRatioDAO = CropRatioDAO()

            cropNameList = cropRatioDAO.viewCropName()

            return render_template('user/addPrediction.html', cityVOList=cityVOList, cropNameList=cropNameList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/ajaxAreaRatioPrediction', methods=['GET'])
def userAjaxAreaRatioPrediction():
    try:
        if adminLoginSession() == 'user':
            cropRatioVO = CropRatioVO()
            cropRatioDAO = CropRatioDAO()
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            cropName = request.args.get('cropName')
            cityId = request.args.get('cityId')

            imageVO.image_CityId = cityId
            imageList = imageDAO.viewImageByCityId(imageVO)
            imageId = imageList[0].imageId

            cropRatioVO.cropName = cropName
            cropRatioVO.cropRatio_ImageId = imageId

            ajaxAreaRatioList = cropRatioDAO.ajaxAreaRationByCropName(cropRatioVO)

            ajaxAreaRatioJson = [i.as_dict() for i in ajaxAreaRatioList]

            return jsonify(ajaxAreaRatioJson)
        else:
            return adminLogoutSession()


    except Exception as ex:
        print(ex)


@app.route('/user/insertPrediction', methods=['POST'])
def userInsertPrediction():
    try:
        if adminLoginSession() == 'user':
            cityVO = CityVO()
            cityDAO = CityDAO()
            cropRatioVO = CropRatioVO()
            cropRatioDAO = CropRatioDAO()
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            prediction_CityId = request.form['prediction_CityId']
            predictionCrop = request.form['predictionCrop']
            predictionYear = time.strftime("%Y")
            print("predictionYear>>>>>"+predictionYear)
            print("predictionYear>>>>>" + predictionYear)
            predictionDate = date.today()
            predictionArea = request.form['predictionArea']
            predictionProduction = request.form['predictionProduction']

            cityVO.cityId = prediction_CityId
            cityList = cityDAO.editCity(cityVO)

            districtName = cityList[0].cityName

            #cropRatioVO.cropRatioId = cropRatioId
            #cropRatioList = cropRatioDAO.cropDetailsByCropRatioId(cropRatioVO)

            #predictionArea = float(cropRatioList[0].cropAreaRatio)

            cropObj = CropPrice_YieldPrediction()
            predictedCropYield, predictedCropPrice = cropObj.cropPrediction(districtName, predictionCrop,
                                                                            predictionYear,
                                                                            predictionArea,
                                                                            predictionProduction)

            loginId = session['session_loginId']
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()
            registerVO.register_LoginId = loginId
            registerList = registerDAO.registerDetailByLoginId(registerVO)
            registerId = registerList[0].registerId

            predictionVO.prediction_CityId = prediction_CityId
            predictionVO.predictionCrop = predictionCrop
            predictionVO.predictionYear = predictionYear
            predictionVO.predictionDate = predictionDate
            predictionVO.predictionArea = predictionArea
            predictionVO.predictionProduction = predictionProduction
            predictionVO.predictionYield = predictedCropYield
            predictionVO.predictionPrice = predictedCropPrice
            predictionVO.prediction_RegisterId = registerId
            predictionDAO.insertPrediction(predictionVO)

            return redirect(url_for('userViewPrediction'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewPrediction', methods=['GET'])
def userViewPrediction():
    try:
        if adminLoginSession() == 'user':
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()
            loginId = session['session_loginId']

            registerVO = RegisterVO()
            registerDAO = RegisterDAO()
            registerVO.register_LoginId = loginId
            registerList = registerDAO.registerDetailByLoginId(registerVO)

            registerId = registerList[0].registerId
            predictionVO.prediction_RegisterId = registerId
            predictionVOList = predictionDAO.viewPrediction(predictionVO)

            return render_template('user/viewPrediction.html', predictionVOList=predictionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewPrediction', methods=['GET'])
def adminViewPrediction():
    try:
        if adminLoginSession() == 'admin':
            predictionDAO = PredictionDAO()

            predictionVOList = predictionDAO.adminViewPrediction()

            return render_template('admin/viewPrediction.html', predictionVOList=predictionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/ajaxGetGraphData')
def userAjaxGetGraphData():
    try:
        if adminLoginSession() == "user":
            register_LoginId = session['session_loginId']
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerVO.register_LoginId = register_LoginId
            registerVOList = registerDAO.registerDetailByLoginId(registerVO)

            select_Crop = request.args.get("select_Crop")
            prediction_RegisterId = registerVOList[0].registerId

            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()
            predictionVO.prediction_RegisterId = prediction_RegisterId
            predictionVO.predictionCrop = select_Crop
            predictionVOList = predictionDAO.userAjaxGetGraphData(predictionVO)

            graphDict = {}
            for i in predictionVOList:
                dict1 = {i[0]: {"Year": i[1], "PredictionYield": i[2], "PredictionPrice": i[3]}}

                graphDict.update(dict1)

            json_object = json.dumps(graphDict)

            var = "var data='" + str(json_object) + "';"

            with open('project/static/adminResources/js/data.json', 'w') as f:
                f.write(var)
            return render_template('user/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadCropByUser')
def adminAjaxDateRegister():
    try:
        if adminLoginSession() == "admin":
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            prediction_RegisterId = request.args.get('select_User')

            predictionVO.prediction_RegisterId = prediction_RegisterId

            ajaxCropVOList = predictionDAO.viewPredictionCrops(predictionVO)

            adminAjaxCropVOList = []
            for i in ajaxCropVOList:
                adminAjaxCropVOList.append(i[0])

            return jsonify(adminAjaxCropVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxGetGraphData')
def adminAjaxGetGraphData():
    try:
        if adminLoginSession() == "admin":

            select_Crop = request.args.get("select_Crop")
            prediction_RegisterId = request.args.get("select_User")

            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            predictionVO.prediction_RegisterId = prediction_RegisterId
            predictionVO.predictionCrop = select_Crop
            predictionVOList = predictionDAO.userAjaxGetGraphData(predictionVO)

            graphDict = {}
            for i in predictionVOList:
                dict1 = {i[0]: {"Year": i[1], "PredictionYield": i[2], "PredictionPrice": i[3]}}

                graphDict.update(dict1)

            json_object = json.dumps(graphDict)

            var = "var data='" + str(json_object) + "';"

            with open('project/static/adminResources/js/admin_data.json', 'w') as f:
                f.write(var)
            return render_template('admin/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deletePrediction', methods=['GET'])
def adminDeletePrediction():
    try:
        if adminLoginSession() == 'user':
            predictionId = request.args.get('predictionId')

            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            predictionVO.predictionId = predictionId

            predictionDAO.userdeletePrediction(predictionVO)
            return redirect(url_for('userViewPrediction'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)

