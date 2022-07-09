import glob
import os
import shutil
from datetime import datetime, date


import cv2
import numpy as np
from flask import request, render_template, redirect, url_for, jsonify,json
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.CityDAO import CityDAO
from project.com.dao.CropRatioDAO import CropRatioDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.OutputDAO import OutputDAO
from project.com.dao.StateDAO import StateDAO
from project.com.vo.CropRatioVO import CropRatioVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.OutputVO import OutputVO
from project.com.vo.CityVO import CityVO


@app.route('/admin/loadImage', methods=['GET'])
def adminLoadimage():
    try:
        if adminLoginSession() == 'admin':

            stateDAO = StateDAO()
            stateVOList = stateDAO.viewState()

            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            return render_template('admin/addImage.html', stateVOList=stateVOList, cityVOList=cityVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertImage', methods=['POST'])
def adminInsertImage():
    try:
        if adminLoginSession() == 'admin':

            cityVO = CityVO()
            imageDAO = ImageDAO()

            UPLOAD_FOLDER = 'project/static/adminResources/inputimages/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            image_StateId = request.form['image_StateId']
            cityName = request.form['image_CityId']

            cityVO.cityName = cityName
            cityVOList = imageDAO.viewCityByCityName(cityVO)
            image_CityId = cityVOList[0].cityId

            imageVO = ImageVO()
            imageDAO = ImageDAO()

            file = request.files['file']
            print(file)

            imageFileName = secure_filename(file.filename)
            imageFilePath = os.path.join(app.config['UPLOAD_FOLDER'])


            imageUploadDate = date.today()

            now = datetime.now()
            imageUploadTime = now.strftime("%H:%M:%S")

            file.save(os.path.join(imageFilePath, imageFileName))

            imageVO.imageFileName = imageFileName

            imageVO.imageFilePath = imageFilePath.replace("project", "..")

            imageVO.imageUploadTime = imageUploadTime

            imageVO.imageUploadDate = imageUploadDate

            imageVO.image_StateId = image_StateId
            imageVO.image_CityId = image_CityId

            imageDAO.insertImage(imageVO)

            # Start Image Crop __________________

            path = imageFilePath + imageFileName
            # print(path)
            img = cv2.imread(path, 1)
            height = img.shape[0]
            width = img.shape[1]
            TotalPixles = height * width  # Total pixles of Main Image

            x, y = 0, 0
            w = w1 = 800
            h = h1 = 800
            n = int(width / w)
            m = int(height / h)
            nw = n * w1  # new width
            nh = m * h1  # new height

            k = 0
            r = 1
            if height > nh:
                m = m + 1
            if width > nw:
                n = n + 1

            directory = 'project/static/adminResources/cropedimages/'
            #foldername = imageFileName.replace('.tif', '')
            foldername = os.path.splitext(imageFileName)[0]
            mypath = directory + foldername
            if not os.path.isdir(mypath):  # creat a folder for save croped images
                os.makedirs(mypath)

            for j in range(m):
                for i in range(n):
                    cropimg = img[y:h, x:w]
                    path = 'project/static/adminResources/cropedimages/' + foldername + '/' + str(r) + ".jpg"
                    cv2.imwrite(path, cropimg)
                    r = r + 1
                    k = k + 1
                    x = w
                    if x == nw:
                        w = width
                    else:
                        w = w + w1
                y = h
                x = 0
                w = w1

                if y == nh:
                    h = height
                else:
                    h = h + h1

            # End CROPING_______________________

            # START DETECT CROP __________________

            outputDAO = OutputDAO()
            rice_cropRatioVO = CropRatioVO()
            jowar_cropRiceVO = CropRatioVO()
            cropRatioDAO = CropRatioDAO()

            path = directory + foldername + '/' + '*.jpg'  # read multiple images for color detection

            Trice_pixles = 0
            Tjowar_pixles = 0
            n = 1  # for image name

            outputpath = 'project/static/adminResources/outputimages/' + foldername
            if not os.path.isdir(outputpath):  # creat a folder for save output images
                os.makedirs(outputpath)

            rice_folder = outputpath + '/' + 'rice'
            if not os.path.isdir(rice_folder):  # creat a folder for save rice detected images
                os.makedirs(rice_folder)

            jowar_folder = outputpath + '/' + 'jowar'
            if not os.path.isdir(jowar_folder):  # creat a folder for save rice detected images
                os.makedirs(jowar_folder)

            for file in glob.glob(path):
                image = cv2.imread(file)

                # Convert BGR to HSV
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # RICE DETECTION______________________

                rice_outputVO = OutputVO()

                outputCrop = 'Rice'

                lower = np.array([12, 85, 162])  # 0  51 255
                upper = np.array([32, 105, 222])

                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(hsv, lower, upper)
                output = cv2.bitwise_and(image, image, mask=mask)

                outputpath = 'project/static/adminResources/outputimages/' + foldername + '/' + outputCrop + '/'
                imagename = 'rice_crop' + str(n) + ".jpg"
                path = outputpath + imagename
                cv2.imwrite(path, output)  # save output images

                rice_pixle = cv2.countNonZero(mask)

                Trice_pixles = Trice_pixles + rice_pixle  # Total detected color pixles of all images

                outputUploadDate = date.today()

                now = datetime.now()
                outputUploadTime = now.strftime("%H:%M:%S")

                rice_outputVO.outputCrop = outputCrop
                rice_outputVO.outputFileName = imagename
                rice_outputVO.outputFilePath = outputpath.replace("project", "..")
                rice_outputVO.outputUploadDate = outputUploadDate
                rice_outputVO.outputUploadTime = outputUploadTime
                rice_outputVO.output_stateId = image_StateId
                rice_outputVO.output_imageId = imageVO.imageId

                rice_cropRatioVO.cropName = outputCrop
                rice_cropRatioVO.cropRatio_ImageId = imageVO.imageId

                # JOWAR DETECTION_______________________

                jowar_outputVO = OutputVO()

                outputCrop = "Jowar"
                lower = np.array([21, 194, 173])  # 0  51 255
                upper = np.array([41, 214, 253])

                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(hsv, lower, upper)
                output = cv2.bitwise_and(image, image, mask=mask)

                outputpath = 'project/static/adminResources/outputimages/' + foldername + '/' + outputCrop + '/'
                imagename = outputCrop + '_crop' + str(n) + ".jpg"
                path = outputpath + imagename
                cv2.imwrite(path, output)  # save output images

                jowar_pixle = cv2.countNonZero(mask)

                Tjowar_pixles = Tjowar_pixles + jowar_pixle  # Total detected color pixles of all images

                outputUploadDate = date.today()

                now = datetime.now()
                outputUploadTime = now.strftime("%H:%M:%S")

                jowar_outputVO.outputCrop = outputCrop
                jowar_outputVO.outputFileName = imagename
                jowar_outputVO.outputFilePath = outputpath.replace("project", "..")
                jowar_outputVO.outputUploadDate = outputUploadDate
                jowar_outputVO.outputUploadTime = outputUploadTime
                jowar_outputVO.output_stateId = image_StateId
                jowar_outputVO.output_imageId = imageVO.imageId

                jowar_cropRiceVO.cropName = outputCrop
                jowar_cropRiceVO.cropRatio_ImageId = imageVO.imageId

                n = n + 1  # For image name

                outputDAO.insertOutput(rice_outputVO, jowar_outputVO)

            rice_Area = (Trice_pixles * 10000) / TotalPixles
            jowar_Area = (Tjowar_pixles * 10000) / TotalPixles

            rice_cropRatioVO.cropAreaRatio = round(rice_Area, 4)
            jowar_cropRiceVO.cropAreaRatio = round(jowar_Area, 4)

            cropRatioDAO.insertCropRatio(rice_cropRatioVO, jowar_cropRiceVO)

            return redirect('/admin/viewImage')

        else:

            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/viewImage', methods=['GET'])
def adminViewImage():
    try:
        if adminLoginSession() == 'admin':
            imageDAO = ImageDAO()
            imageVOList = imageDAO.viewImage()
            return render_template('admin/viewImage.html', imageVOList=imageVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/editImage', methods=['GET'])
def adminEditImage():
    try:
        if adminLoginSession() == 'admin':

            imageId = request.args.get('imageId')

            imageVO = ImageVO()
            imageDAO = ImageDAO()
            stateDAO = StateDAO()

            imageVO.imageId = imageId

            stateVOList = stateDAO.viewState()

            imageVOList = imageDAO.editImage(imageVO)

            return render_template('admin/editImage.html', stateVOList=stateVOList, imageVOList=imageVOList)
        else:

            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/updateImage', methods=['POST'])
def adminUpdateImage():
    try:
        if adminLoginSession() == 'admin':

            imageId = request.form['imageId']

            image_StateId = request.form['image_StateId']
            imageFileName = request.form['imageFileName']
            imageFilePath = request.form['imageFilePath']

            imageUploadDate = date.today()
            now = datetime.now()
            imageUploadTime = now.strftime("%H:%M:%S")

            imageVO = ImageVO()
            imageDAO = ImageDAO()

            imageVO.imageId = imageId

            imageVO.image_StateId = image_StateId
            imageVO.imageFileName = imageFileName
            imageVO.imageFilePath = imageFilePath
            imageVO.imageUploadDate = imageUploadDate
            imageVO.imageUploadTime = imageUploadTime

            imageDAO.updateImage(imageVO)

            return redirect('/admin/viewimage')
        else:

            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteImage', methods=['GET'])
def adminDeleteImage():
    try:
        if adminLoginSession() == 'admin':
            imageId = request.args.get('imageId')
            imageDAO = ImageDAO()

            imageDAO.deleteOutput(imageId)
            imageList = imageDAO.deleteImage(imageId)

            path = '../static/adminResources/outputimages/' + imageList.imageFileName.replace('.tif', '')
            shutil.rmtree(path)

            path = imageList.imageFilePath.replace("..", "project") + imageList.imageFileName

            os.remove(path)

            return redirect(url_for('adminViewimage'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/viewoutput', methods=['GET'])
def adminViewOutput():
    try:
        if adminLoginSession() == 'admin':
            imageDAO = ImageDAO()
            outputVO = OutputVO()
            outputVO.output_imageId = request.args.get('imageId')
            outputVOList = imageDAO.viewOutput(outputVO)
            return render_template('admin/viewOutput.html', outputVOList=outputVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/user/viewImage', methods=['GET'])
def userViewImage():
    try:
        if adminLoginSession() == 'user':
            imageDAO = ImageDAO()
            imageVOList = imageDAO.viewImage()

            return render_template('user/viewImage.html', imageVOList=imageVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/viewoutput', methods=['GET'])
def userViewOutput():
    try:
        if adminLoginSession() == 'user':

            imageDAO = ImageDAO()
            outputVO = OutputVO()

            outputVO.output_imageId = request.args.get('imageId')
            outputVOList = imageDAO.viewOutput(outputVO)

            return render_template('user/viewOutput.html', outputVOList=outputVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)

@app.route('/admin/ajaxLoadCityByState')
def adminAjaxCityData():
    try:
        if adminLoginSession() == "admin":
            cityVO = CityVO()
            cityDAO = CityDAO()

            city_StateId = request.args.get('image_StateId')
            cityVO.city_StateId = city_StateId

            ajaxCropVOList = cityDAO.viewCityDetailsByState(cityVO)

            adminAjaxCityVOList = []
            for i in ajaxCropVOList:
                adminAjaxCityVOList.append(i)

            return jsonify(adminAjaxCityVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)

