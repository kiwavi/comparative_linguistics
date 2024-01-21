# contains pydantic models (data shape)

from pydantic import BaseModel

class WordsBase(BaseModel):
    # common attributes for reading and creating words
    id:int
    english_word: str
    language_word_equivalent: str
    language_id: int

class WordsCreate(WordsBase):
    # creating words
    description: str
    language_fam_id: str
    user_id: int
    creation_date: date
    deletion_date: date
    
class UserBase(BaseModel):
    # common attributes for reading and creating users
    id: int
    email: str
    
class UserCreate(UserBase):
    # creating users
    hashed_password: str
    is_active: bool
    creation_date: date
    
class LanguageBase(BaseModel):
    # common attributes for reading and creating languages
    id:int
    name: str
    language_description: str


class LanguageCreate(LanguageBase):
    # creating languages
    creation_date: date
    language_family_id: id
    
class LanguageFamilyBase(BaseModel):
    # common attributes for reading and creating language families
    id:int
    name: str
    language_family_description: str
    creation_date: date

class LanguageFamilyCreate(LanguageFamilyBase):
    # create language families
    pass

class WordListBase(BaseModel):
    # common attributes for reading and creating wordlist
    id:int
    word: str
    creation_date: str
    # picture:

class WordListCreate(WordListBase):
    # creating wordlist
    pass
    