from project import db

from project.com.vo.LoginVO import LoginVO


class UserDAO:

    def validateUser(self, loginVO):

        userlist = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginRole=loginVO.loginRole)
        return userlist

    def updatePassword(self, loginVO):  # forgot password
        db.session.merge(loginVO)
        db.session.commit()

    def chagePassword(self, loginVO):  # user chnage password
        userList = LoginVO.query.filter_by(loginId=loginVO.loginId).first()

        if loginVO.loginPassword is None:
            return userList
        else:
            db.session.merge(loginVO)
            db.session.commit()
