from project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class ComplainDAO:
    def insertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def userViewComplain(self, complainVO):
        complainList = db.session.query(ComplainVO) \
            .filter(ComplainVO.complainFrom_LoginId == complainVO.complainFrom_LoginId).all()

        return complainList

    def adminViewComplain(self):
        adminComplainList = db.session.query(ComplainVO, LoginVO, RegisterVO) \
            .join(LoginVO, ComplainVO.complainFrom_LoginId == LoginVO.loginId) \
            .join(RegisterVO, LoginVO.loginId == RegisterVO.register_LoginId).all()

        return adminComplainList

    def deleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)
        db.session.delete(complainList)
        db.session.commit()
        return complainList

    def insertComplainReply(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()

    def viewComplainReply(self, complainVO):
        complainList = db.session.query(ComplainVO) \
            .filter(ComplainVO.complainId == complainVO.complainId)
        return complainList

    def userTotalPendingComplain(self, complainVO):
        complainList = db.session.query(ComplainVO) \
            .filter(ComplainVO.complainFrom_LoginId == complainVO.complainFrom_LoginId) \
            .filter(ComplainVO.complainStatus == complainVO.complainStatus).all()
        return complainList

    def adminTotalPendingComplain(self, complainVO):
        complainList = db.session.query(ComplainVO) \
            .filter(ComplainVO.complainStatus == complainVO.complainStatus).all()
        return complainList
