from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base, CommonFieldsMixin


class Donation(CommonFieldsMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)
    user = relationship("User")
