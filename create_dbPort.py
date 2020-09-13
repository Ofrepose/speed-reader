import sys
import os
import sqlalchemy
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin

Base = declarative_base()



class User(UserMixin, Base):
	__tablename__ = 'user'

	name_first = Column(
		String(80), nullable = False)

	name_last = Column(
		String(80), nullable = False)


	email = Column(
		String(150), nullable = False)

	image = Column(
		String(80))

	p = Column (
		String(80), nullable = False)

	pValid = Column (
		Integer, default = 1 )

	privelage = Column(
		Integer, default = 1)

	initial_key = Column (
		BigInteger)

	is_validated = Column(
		String(80), default = 'no')

	id = Column(
		Integer, primary_key = True)
	
class Project(Base):
	__tablename__ ='project'

	id = Column(
		Integer, primary_key = True)
	
		# 1 = Residential 2 = Commercial
	p_type= Column(
		Integer) 

	name_last = Column(
		String(80))

	name_first = Column(
		String(80))

	cli_email = Column(
		String(80))

	cli_phone = Column(
		String(80))

	cli_phone2 = Column(
		String(80))

	cli_add = Column(
		String(80))

	cli_add2 = Column(
		String(80))

	cli_city = Column(
		String(80))

	cli_state = Column(
		String(80))

	cli_zip = Column(
		String(80))

	notes = Column(
		Text())

	instructions = Column(
		Text())

	completed = Column(
		Integer)

	note_owner = Column(
		String(80))

	instruction_owner = Column(
		String(80))



class Images(Base):
	__tablename__  = 'images'

	id = Column(
		Integer, primary_key = True)

	name = Column(
		String(80))

	client_id = Column(
		Integer, ForeignKey('project.id'))
	 
	project = relationship (Project)

class Notes(Base):
	__tablename__ = 'notes'

	id = Column(
		Integer, primary_key = True)

	content = Column(
		Text())

	client_id = Column(
		Integer, ForeignKey('project.id'))
	 
	project = relationship (Project)

	owner_id = Column(
		Integer, ForeignKey('user.id'))

	user = relationship(User)






class Product(Base):
	__tablename__ = 'product'

	id = Column(
		Integer, primary_key = True)

	photo_name = Column(
		String(190))	

	client_id = Column(
		Integer, ForeignKey('project.id'))

	project = relationship(Project)

	name = Column(
		String(80))

	price= Column(
		String(90))

	description = Column(
		String(200))

	upi = Column(
		String(190))



class Room(Base):
	__tablename__ = 'room'

	id = Column(
		Integer, primary_key = True)

	room_type = Column(
		String(80))

	unique_name = Column(
		String(80))

	# 0 = false 1 = true
	master = Column(
		Integer, default = 0)

	

	product_amount = Column(
		Integer, default = 0)

	client_id = Column(
		Integer, ForeignKey('project.id'))
	 
	project = relationship (Project)

	instructions = Column(
		Text())
	completed = Column(
		Integer, default = 0)







class cust_Product(Base):
	__tablename__ = 'cust_product'

	id = Column(
		Integer, primary_key = True)

	client_id = Column(
		Integer, ForeignKey('project.id'))

	project = relationship(Project)

	product_id = Column(
		Integer, ForeignKey('product.id'))

	room_id = Column(
		Integer, ForeignKey('room.id'))
	room = relationship(Room)



	product = relationship(Product)





class UserB(UserMixin, Base):
	__tablename__ = 'userb'

	id = Column(
		Integer, primary_key = True)

	email = Column(
		String(80))

	p_word = Column(
		String(80))

	name_first = Column(
		String(180))

	name_last = Column(
		String(180))

	rating = Column(
		Integer, default = 0)


class Book(Base):
	__tablename__ = 'book'

	id = Column(
		Integer, primary_key = True)

	owner_id = Column(
		Integer, ForeignKey('userb.id'))

	userb = relationship(UserB)

	filename = Column(
		String(180))

	name = Column(
		String(180))								

	author = Column(
		String(180))

	shared = Column(
		Integer, default = 0)

	content = Column(
		Text())

	save_loc = Column(
		Integer, default = 0)

	mem = Column(
		Text())

	mem_count = Column(
		Integer, default = 0)

	compat = Column(
		Integer)



class UserBL(Base):
	__tablename__ = "userbl"

	id = Column(
		Integer,primary_key = True)

	owner_id = Column(
		Integer, ForeignKey('user.id'))

	user = relationship(User)

	book_id = Column(
		Integer, ForeignKey('book.id'))

	book = relationship(Book)

	

class Words(Base):
	__tablename__ = 'words'

	id = Column(
		Integer, primary_key = True)


	content = Column(
		Text())

	save_loc = Column(
		Integer, default = 0)

	mem = Column(
		Text())

	mem_count = Column(
		Integer, default = 0)

class SiteSurvey(Base):
	__tablename__ = 'sitesurver'

	id = Column(
		Integer, primary_key = True)
	
	cust_name = Column(
		Text(), nullable = False)

	cust_phone = Column(
		Text())

	cust_street = Column(
		Text(), nullable = False)

	db_range = Column(
		Text())
	
	notes = Column(
		Text())

	image = Column(
		Text())
	m_ID = Column(
		Text())
	m_E01 =Column(
		Text())
	m_E02=Column(
		Text())
	mSN=Column(
		Text())
	aPn=Column(
		Text())
	aIMEI=Column(
		Text())
	aSN=Column(
		Text())
	aMAC=Column(
		Text())
	aGAIN=Column(
		Text())
	status = Column(
		Text())












engine = create_engine('sqlite:///ac_db_be.db')
Base.metadata.create_all(engine)

