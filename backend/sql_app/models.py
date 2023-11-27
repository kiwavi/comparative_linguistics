from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

# fields i should add are deleted_at, createdat to every table. They should be null by default because we'll be doing migrations.  

class Words():
    __tablename__ = 'words'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # relationships
    user_lang_id = Column(Integer,ForeignKey("languages.id"))
    language_fam_id = Column(Integer,ForeignKey("language_families.id")) # not so necessary though

    user_lang = relationship("Languages", back_populates="words")
    language_fam = relationship("Language_Families", back_populates="words_fam")

class Languages():
    __tablename__ = 'languages'

    name = Column(String, index=True)
    language_description = Column(String, index=True)
    language_family_id = Column(Integer,ForeignKey("language_families.id"))

    language_family = relationship("Language_Families", back_populates="lang")
    words = relationship("Words", back_populates="user_lang")
    
class Language_Families():
    __tablename__ = 'language_families'
    
    name = Column(String, index=True)
    language_family_description = Column(String, index=True)

    words_fam = relationship("Words", back_populates="language_fam")
    lang = relationship("Languages", back_populates="language_family")
    
class WordList():
    __tablename__ = 'wordlist'

    word = Column(String, index=True)
    picture = image_attachment('WordPicture')

class WordPicture(Base, Image):
    wordlist_id = Column(Integer,ForeignKey('user.id'),primary_key=True)
    wordlist = relationship('WordList')
    __tablename__ = 'word_picture'
