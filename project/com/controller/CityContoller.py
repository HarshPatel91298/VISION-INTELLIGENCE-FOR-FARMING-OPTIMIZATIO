from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.CityDAO import CityDAO
from project.com.dao.StateDAO import StateDAO
from project.com.vo.CityVO import CityVO


@app.route('/admin/loadCity', methods=['GET'])
def adminLoadCity():
    try:
        if adminLoginSession() == 'admin':
            stateDAO = StateDAO()
            stateVOList = stateDAO.viewState()

            return render_template('admin/addCity.html', stateVOList=stateVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/insertCity', methods=['POST'])
def adminInsertCity():
    try:
        if adminLoginSession() == 'admin':

            cityName = request.form['cityName']
            cityDescription = request.form['cityDescription']
            city_StateId = request.form['city_StateId']

            cityVO = CityVO()
            cityDAO = CityDAO()

            cityVO.cityName = cityName
            cityVO.cityDescription = cityDescription
            cityVO.city_StateId = city_StateId

            cityDAO.insertCity(cityVO)

            return redirect(url_for('adminViewCity'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/viewCity', methods=['GET'])
def adminViewCity():
    try:
        if adminLoginSession() == 'admin':
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()
            return render_template('admin/viewCity.html', cityVOList=cityVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCity', methods=['GET'])
def adminDeleteCity():
    try:
        if adminLoginSession() == 'admin':
            cityId = request.args.get('cityId')

            cityDAO = CityDAO()
            cityVO = CityVO()

            cityVO.cityId = cityId

            cityDAO.deleteCity(cityVO)

            return redirect(url_for('adminViewCity'))
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/editCity', methods=['GET'])
def adminEditCity():
    try:
        if adminLoginSession() == 'admin':
            cityId = request.args.get('cityId')

            cityVO = CityVO()

            cityDAO = CityDAO()
            stateDAO = StateDAO()

            cityVO.cityId = cityId

            cityVOList = cityDAO.editCity(cityVO)

            stateVOList = stateDAO.viewState()

            return render_template('admin/editCity.html', stateVOList=stateVOList, cityVOList=cityVOList)
        else:
            return redirect('/admin/logoutSession')

    except Exception as ex:
        print(ex)


@app.route('/admin/updateCity', methods=['POST'])
def adminUpdateCity():
    try:
        if adminLoginSession() == 'admin':
            cityName = request.form['cityName']
            cityDescription = request.form['cityDescription']
            city_StateId = request.form['city_StateId']
            cityId = request.form['cityId']

            cityVO = CityVO()
            cityDAO = CityDAO()

            cityVO.cityId = cityId
            cityVO.cityName = cityName
            cityVO.cityDescription = cityDescription
            cityVO.city_StateId = city_StateId

            cityDAO.updateCity(cityVO)

            return redirect(url_for('adminViewCity'))
        else:

            return redirect('/admin/logoutSession')
    except Exception as ex:

        print(ex)
