from project import db


class LoginVO(db.Model):
    __tablename__ = 'loginmaster'
    loginId = db.Column('loginId', db.Integer, primary_key=True, autoincrement=True)
    loginUsername = db.Column('loginUsername', db.VARCHAR(100), unique=True, nullable=False)
    loginPassword = db.Column('loginPassword', db.String(16), nullable=False)
    loginRole = db.Column('loginRole', db.String(10), nullable=False)
    loginStatus = db.Column('loginStatus', db.String(10), nullable=False)

    def as_dict(self):
        return {
            'loginId': self.loginId,
            'loginUsername': self.loginUsername,
            'loginPassword': self.loginPassword,
            'loginRole': self.loginRole,
            'loginStatus': self.loginStatus
        }


db.create_all()
