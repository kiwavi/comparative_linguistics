# contains pydantic models (data shape)

from pydantic import BaseModel
from datetime import datetime,date
from pydantic import ConfigDict

class WordsBase(BaseModel):
    # common attributes for reading and creating words    
    english_word: str
    language_word_equivalent: str
    language_id: int

class WordsCreate(WordsBase):
    # creating words
    description: str
    user_id: int
    
class UserBase(BaseModel):
    # common attributes for reading and creating users
    email: str
    username: str
    
class UserCreate(UserBase):
    # creating users
    password: str

    class Config:
        orm_mode = True
        
class UserOut(UserBase):
    id: int
    creation_date: datetime

class LanguageBase(BaseModel):
    # common attributes for reading and creating languages    
    name: str
    language_description: str


class LanguageCreate(LanguageBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # creating languages
    name: str
    language_description: str    
    language_family_id: int

class LanguagesOut(LanguageCreate):
    id: int
    
class LanguageFamilyBase(BaseModel):
    # common attributes for reading and creating language families    
    name: str
    language_family_description: str
    # creation_date: datetime

class LanguageFamilyCreate(LanguageFamilyBase):
    # create language families
    pass

class LanguageFamilyOut(LanguageFamilyBase):
    id: int
    creation_date: datetime

class WordListBase(BaseModel):
    # common attributes for reading and creating wordlist 
    word: str

class WordListOut(WordListBase):
    # creating wordlist
    id: int


class WordPictureBase(BaseModel):
    wordlist_id: int

class WordPicOut(WordPictureBase):
    id: int
