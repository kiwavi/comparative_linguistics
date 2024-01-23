from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment
from datetime import datetime

class Language_Families(Base):
    __tablename__ = 'language_families'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True)
    language_family_description = Column(String, index=True, nullable=True)
    creation_date = Column(DateTime, default=datetime.now(), nullable=True,)
    deletion_date = Column(DateTime, nullable=True,)
    
    words_fam = relationship("Words", back_populates="language_fam")
    lang = relationship("Languages", back_populates="language_family")


class Languages(Base):
    __tablename__ = 'languages'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True)
    language_description = Column(String, index=True, nullable=True)
    language_family_id = Column(Integer,ForeignKey("language_families.id"),nullable=True)
    creation_date = Column(DateTime,default=datetime.now(), nullable=True)
    deletion_date = Column(DateTime,nullable=True,)

    language_family = relationship("Language_Families", back_populates="lang")
    words = relationship("Words", back_populates="user_lang")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    creation_date = Column(DateTime,default=datetime.now(),nullable=True)
    deletion_date = Column(DateTime, nullable=True)
    # relationships
    user_lang_id = Column(Integer,ForeignKey("languages.id"),nullable=True)
    language_fam_id = Column(Integer,ForeignKey("language_families.id"),nullable=True) # not so necessary though
    user_lang = relationship("Languages", back_populates="words")
    language_fam = relationship("Language_Families", back_populates="words_fam")
    words = relationship("Words", back_populates="user")
    
class Words(Base):
    __tablename__ = 'words'
    
    id = Column(Integer,primary_key=True,index=True)
    english_word = Column(String, index=True)
    language_word_equivalent = Column(String, index=True)
    description = Column(String, index=True, nullable=True)        
    language_id = Column(Integer,ForeignKey("languages.id"),nullable=True)
    language_fam_id = Column(Integer,ForeignKey("language_families.id"),nullable=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=True)
    creation_date = Column(DateTime, default=datetime.now(), nullable=True)
    deletion_date = Column(DateTime, nullable=True,)

    language = relationship("Languages", back_populates="words")
    language_fam = relationship("Language_Families", back_populates="words_fam")
    user = relationship("users", back_populates="words")
    
class WordList(Base):
    __tablename__ = 'wordlist'

    id = Column(Integer,primary_key=True,index=True)
    word = Column(String, index=True)
    creation_date = Column(DateTime, nullable=True)
    deletion_date = Column(DateTime, nullable=True)

    picture = image_attachment('WordPicture')

class WordPicture(Base, Image):
    __tablename__ = 'wordpicture'

    wordlist_id = Column(Integer,ForeignKey("wordlist.id"))
    creation_date = Column(DateTime, default=datetime.now(), nullable=True)
    deletion_date = Column(DateTime, nullable=True,)
    
    wordlist = relationship('WordList')
