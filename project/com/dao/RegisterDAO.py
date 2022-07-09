from project import db

from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.StateVO import StateVO


class RegisterDAO:
    def insertregister(self, registerVO):
        db.session.add(registerVO)
        db.session.commit()

    def viewUser(self):
        userlist = db.session.query(RegisterVO, LoginVO, StateVO, CityVO) \
            .join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId) \
            .join(StateVO, RegisterVO.register_StateId == StateVO.stateId) \
            .join(CityVO, RegisterVO.register_CityId == CityVO.cityId).all()

        return userlist

    def updateUserStatus(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def registerDetailByLoginId(self, registerVO):
        registerList = RegisterVO.query.filter_by(register_LoginId=registerVO.register_LoginId).all()
        return registerList

    def editProfile(self, registerVO):
        registerList = db.session.query(RegisterVO, LoginVO) \
            .join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId) \
            .filter(RegisterVO.register_LoginId == registerVO.register_LoginId).all()
        return registerList

    def updateRegister(self, registerVO):
        db.session.merge(registerVO)
        db.session.commit()
