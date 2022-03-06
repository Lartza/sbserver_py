from pydantic import BaseModel


class Vipusers(BaseModel):
    userID: str


class Sponsortimes(BaseModel):
    videoID: str
    startTime: float
    endTime: float
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
    videoDuration: int
    hidden: int
    reputation: float
    shadowHidden: int
    hashedVideoID: str
    userAgent: str
    description: str


class Usernames(BaseModel):
    userID: str
    userName: str
    locked: int


class Config(BaseModel):
    key: str
    value: str


class SponsortimeListPaginated(BaseModel):
    items: list[Sponsortimes]
    next_page_token: int | None
    size: int
