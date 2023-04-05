from sqlalchemy import Column, Text, REAL, Integer, BigInteger

from database import Base


class Vipusers(Base):
    __tablename__ = 'vipUsers'

    userID = Column(Text, nullable=False, primary_key=True)


class Sponsortimes(Base):
    __tablename__ = 'sponsorTimes'

    videoID = Column(Text, nullable=False)
    startTime = Column(REAL, nullable=False)
    endTime = Column(REAL, nullable=False)
    votes = Column(Integer, nullable=False)
    locked = Column(Integer, nullable=False, default=0)
    incorrectVotes = Column(Integer, nullable=False, default=1)
    UUID = Column(Text, nullable=False, primary_key=True)
    userID = Column(Text, nullable=False)
    timeSubmitted = Column(BigInteger, nullable=False)
    views = Column(Integer, nullable=False)
    category = Column(Text, nullable=False, default='sponsor')
    actionType = Column(Text, nullable=False, default='skip')
    service = Column(Text, nullable=False, default='YouTube')
    videoDuration = Column(REAL, nullable=False, default=0)
    hidden = Column(Integer, nullable=False, default=0)
    reputation = Column(REAL, nullable=False, default=0)
    shadowHidden = Column(Integer, nullable=False)
    hashedVideoID = Column(Text, nullable=False, default='')
    userAgent = Column(Text, nullable=False, default='')
    description = Column(Text, nullable=False, default='')


class Usernames(Base):
    __tablename__ = 'userNames'

    userID = Column(Text, nullable=False, primary_key=True)
    userName = Column(Text, nullable=False)
    locked = Column(Integer, nullable=False, default=0)


class Config(Base):
    __tablename__ = 'config'

    key = Column(Text, nullable=False, primary_key=True)
    value = Column(Text, nullable=False)
