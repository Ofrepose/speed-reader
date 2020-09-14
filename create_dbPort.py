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


engine = create_engine('sqlite:///ac_db_be.db')
Base.metadata.create_all(engine)

