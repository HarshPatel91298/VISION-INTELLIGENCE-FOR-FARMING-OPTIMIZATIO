from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def validateLogin(self, loginVO):
        loginList = db.session.query(LoginVO).filter(LoginVO.loginUsername == loginVO.loginUsername,
                                                     LoginVO.loginPassword == loginVO.loginPassword)

        return loginList

    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def viewLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginId=loginVO.loginId).all()
        return loginList

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()
