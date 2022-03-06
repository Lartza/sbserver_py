from sqlalchemy import MetaData, Table, Column, Text, REAL, Integer

metadata = MetaData()

vipusers = Table(
    'vipUsers',
    metadata,
    Column('userID', Text, nullable=False, index=True, primary_key=True)
)

sponsortimes = Table(
    'sponsorTimes',
    metadata,
    Column('videoID', Text, nullable=False),
    Column('startTime', REAL, nullable=False),
    Column('endTime', REAL, nullable=False),
    Column('votes', Integer, nullable=False),
    Column('locked', Integer, nullable=False, default=0),
    Column('incorrectVotes', Integer, nullable=False, default=1),
    Column('UUID', Text, nullable=False, unique=True, index=True, primary_key=True),
    Column('userID', Text, nullable=False, index=True),
    Column('timeSubmitted', Integer, nullable=False, index=True),
    Column('views', Integer, nullable=False),
    Column('category', Text, nullable=False, default='sponsor'),
    Column('actionType', Text, nullable=False, default='skip'),
    Column('service', Text, nullable=False, default='Youtube'),
    Column('videoDuration', Integer, nullable=False, default=0),
    Column('hidden', Integer, nullable=False, default=0),
    Column('reputation', REAL, nullable=False, default=0),
    Column('shadowHidden', Integer, nullable=False),
    Column('hashedVideoID', Text, nullable=False, default=''),
    Column('userAgent', Text, nullable=False, default=''),
    Column('description', Text, nullable=False, default=''),
)

usernames = Table(
    'userNames',
    metadata,
    Column('userID', Text, nullable=False, unique=True, index=True, primary_key=True),
    Column('userName', Text, nullable=False),
    Column('locked', Integer, nullable=False, default=0)
)

config = Table(
    'config',
    metadata,
    Column('key', Text, nullable=False, unique=True, primary_key=True),
    Column('value', Text, nullable=False)
)
