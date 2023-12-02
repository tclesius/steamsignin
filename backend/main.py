from datetime import timedelta
from datetime import datetime
import socket
from typing import Annotated, Dict
from fastapi import security
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy import Boolean, create_engine, Column, String, Integer, MetaData, Table, select
from sqlalchemy.orm import sessionmaker, declarative_base
from steampowered import SteamPowered
from steamopenid import OpenIDResponse, SteamOpenID
from sqlalchemy.orm import Session
import jwt
from fastapi.middleware.cors import CORSMiddleware
from datetime import UTC


SQLALCHEMY_DATABASE_URL = "postgresql://test:test@localhost/steamsignin"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
EXPIRE_MINUTES = 30

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
	__tablename__ = "users"	
	steamid = Column(String, primary_key=True)
	communityvisibilitystate = Column(Integer)
	profilestate = Column(Integer)
	personaname = Column(String, index=True)
	commentpermission = Column(String)
	profileurl = Column(String)
	avatar = Column(String)
	avatarmedium = Column(String)
	avatarfull = Column(String)
	avatarhash = Column(String)
	lastlogoff = Column(String)
	personastate = Column(String)
	personastate = Column(String)
	primaryclanid = Column(String)
	timecreated = Column(String)
	personastateflags = Column(String)
	loccountrycode = Column(String)
	locstatecode = Column(String)
	lastlogoff = Column(String)


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def get_session():
	with SessionLocal() as session:
		yield session

class ServiceException:
	TOKEN_EXCEPTION = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Not authenticated",
		headers={"WWW-Authenticate": "Bearer"},
	)
	NOT_AUTHORIZED_TO_SEE_RESSOURCE = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Not authorized to see this ressource",
	)
	MALFORMED_OPENID_RESPONSE =  HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Malformed OpenID response",
	)

def create_access_token(steamid: str, expires_delta: timedelta = timedelta(minutes=15)):
	expire = datetime.now(UTC) + expires_delta
	encoded_jwt = jwt.encode({"exp": expire, "sub": steamid}, SECRET_KEY, algorithm="HS256")
	return encoded_jwt

security = HTTPBearer()

async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: Annotated[Session, Depends(get_session)]):
	try:
		token = credentials.credentials
		payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
		steamid: str = payload.get("sub")

		if steamid is None:
			raise ServiceException.TOKEN_EXCEPTION
	except Exception:
		raise ServiceException.TOKEN_EXCEPTION
	
	if not (user := session.get(User, steamid)):
		raise ServiceException.TOKEN_EXCEPTION
	return user



app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
	"http://localhost:5173",
	"http://localhost",
	"http://0.0.0.0",
	"http://0.0.0.0:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/auth/steam/callback') 
async def callback(openid_response: OpenIDResponse, session: Annotated[Session, Depends(get_session)]):
	if steamid := SteamOpenID.validate(openid_response):
		player_summary = SteamPowered.get_player_summaries([steamid])["response"]["players"][0]

		if user := session.query(User).where(User.steamid == steamid).first():
			for key, value in player_summary.items():
				# we should update user infos on every login to be sure all data is current (profile picture etc. )
				# alternatively and i would prefer to update all user profiles with a background task cron daily. 
				# We can then update multiple accounts at once too bc. the webapi route get_player_summaries supports it.
				setattr(user, key, value)
			session.add(user)
			session.commit()
		else:
			user = User(**player_summary)
			session.add(user)
			session.commit()
		access_token = create_access_token(str(user.steamid))
		return {"access_token": access_token, "token_type": "bearer"}
	else:
		return ServiceException.TOKEN_EXCEPTION


@app.get("/me")
async def get_profile(user: Annotated[User, Depends(get_current_user)]):
	return user




if __name__ == '__main__':
	ip_address = socket.gethostbyname(socket.gethostname())
	print("Network: http://" + ip_address + ":8080")
	uvicorn.run(app, host="0.0.0.0", port = 8080)

