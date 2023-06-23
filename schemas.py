# pylint:disable=too-few-public-methods
from pydantic import BaseModel, validator


class VipusersBase(BaseModel):
    userID: str


class Vipusers(VipusersBase):
    class Config:
        orm_mode = True


class SponsortimesBase(BaseModel):
    videoID: str
    startTime: float
    endTime: float
    length: float
    votes: int
    locked: int
    incorrectVotes: int
    UUID: str
    userID: str
    timeSubmitted: int
    views: int
    category: str
    actionType: str
    service: str
    videoDuration: float
    hidden: int
    reputation: float
    shadowHidden: int
    hashedVideoID: str
    userAgent: str
    description: str
    userName: str | None


class Sponsortimes(SponsortimesBase):
    @validator('shadowHidden')
    def shadowhidden(cls, value: int) -> int:
        if value <= 0:
            return 0
        return 1

    class Config:
        orm_mode = True


class UsernamesBase(BaseModel):
    userID: str
    userName: str
    locked: int


class Usernames(UsernamesBase):
    class Config:
        orm_mode = True


class ConfigBase(BaseModel):
    key: str
    value: str


class Config(ConfigBase):
    class Config:
        orm_mode = True
