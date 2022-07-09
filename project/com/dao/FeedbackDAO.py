from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class FeedbackDAO:
    # User Side
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def userViewFeedback(self, feedbackVO):
        feedbackList = db.session.query(FeedbackVO) \
            .filter(FeedbackVO.feedbackFrom_LoginId == feedbackVO.feedbackFrom_LoginId).all()

        return feedbackList

    def deleteFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.get(feedbackVO.feedbackId)
        db.session.delete(feedbackList)
        db.session.commit()

    # Admin Side

    def adminViewFeedback(self):
        adminFeedbackList = db.session.query(FeedbackVO, LoginVO, RegisterVO) \
            .join(LoginVO, FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId) \
            .join(RegisterVO, LoginVO.loginId == RegisterVO.register_LoginId).all()

        return adminFeedbackList

    def adminReviewFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()
