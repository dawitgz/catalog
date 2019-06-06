from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key = True)
  name = Column(String(80), nullable=False)
  email = Column(String(80), nullable=True)
  picture = Column(String(150))

  @property
  def serialize(self):
  	return {
      'name' : self.name,
      'email' : self.email
    }

class Category(Base):
  __tablename__ = 'category'

  id = Column(Integer, primary_key = True)
  name = Column(String(250), nullable=False)

  @property
  def serialize(self):
  	return self.name

class SportItem(Base):
  __tablename__ = 'sportitem'

  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  description = Column(String(500))

  category_id = Column(Integer, ForeignKey('category.id'))
  category = relationship(Category)

  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship(User)	

  @property
  def serialize(self):
  	return {
  		'id' : self.id,
  		'name' : self.name,
  		'description' : self.description,
  		'user' : self.user.serialize,
      'category': self.category.serialize
  	}
  


engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
 
Base.metadata.create_all(engine)  
