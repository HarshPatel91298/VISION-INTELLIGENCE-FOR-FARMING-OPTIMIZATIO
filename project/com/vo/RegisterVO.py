from project import db

from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.StateVO import StateVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    registerCompanyname = db.Column('registerCompanyname', db.String(100), nullable=False)
    registerAddress = db.Column('registerAddress', db.String(100), nullable=False)
    registerContactNumber = db.Column('registerContactNumber', db.VARCHAR(10), nullable=False)
    register_StateId = db.Column('register_StateId', db.Integer, db.ForeignKey(StateVO.stateId))
    register_CityId = db.Column('register_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerCompanyname': self.registerCompanyname,
            'registerAddress': self.registerAddress,
            'registerContactNumber': self.registerContactNumber,
            'register_StateId': self.register_StateId,
            'register_CityId': self.register_CityId,
            'register_LoginId': self.register_LoginId

        }


db.create_all()
