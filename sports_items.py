from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import SportItem, Base, Category, User
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Users
user1 = User(name='Dawit Bekele', email='dawit.g.bekele@gmail.com', picture='')
session.add(user1)
session.commit()

user2 = User(name='John Doe', email='john.doe@email.com', picture='')
session.add(user2)
session.commit()

#Items for Soccer
category1 = Category(name = "Soccer")
session.add(category1)
session.commit()


sportItem1 = SportItem(name = "Shinguards", description = "shinguard to protect the shins", category = category1, user = user1)

session.add(sportItem1)
session.commit()

sportItem2 = SportItem(name = 'Two shinguards', description=" two shinguards", category=category1, user=user2)
session.add(sportItem2)
session.commit()

sportItem3 = SportItem(name= "Jersey", description="Soccer team jersey", category=category1, user=user1)
session.add(sportItem3)
session.commit()

sportItem4 = SportItem(name="Soccer Cleats", description="soccer cleats", category=category1, user=user2)
session.add	(sportItem4)
session.commit()


#Items for Snow Boarding
category2 = Category(name = "Snowboarding")
session.add(category2)
session.commit()

sportItem5 = SportItem(name = "Snowboard", description = "Best for any terrain and conditions. All-mountain snowboards perform anywhere on a mountain - groomed runs, backcountry, even park and pipe. They may be direectional (meaning downlhill only) or twin-tip (for riding switch, meaning either direction). Most boarders ride all-mountain boards. Because of their versatility, all-mountain boards are good for beginners who are still learning what terrain they like.", category = category2, user = user1)

session.add(sportItem5)
session.commit()

sportItem6 = SportItem(name = 'Googles', description="Googles that protect eyes from the snowy glare.", category=category2, user=user2)
session.add(sportItem6)
session.commit()


#Items for Hockey
category3 = Category(name = "Hockey")
session.add(category3)
session.commit()

sportItem7 = SportItem(name = "Stick", description = "Hockey sticks to beat your opponent with.", category = category3, user = user1)

session.add(sportItem7)
session.commit()

sportItem8 = SportItem(name = 'puck', description="hockey puck.", category=category3, user=user2)
session.add(sportItem8)
session.commit()

#Items for Baseball
category4 = Category(name = "Baseball")
session.add(category4)
session.commit()

sportItem9 = SportItem(name = "Bat", description = "Baseball bat", category = category4, user = user1)

session.add(sportItem9)
session.commit()

#Items for Basketball
category5 = Category(name = "Basketball")
session.add(category5)
session.commit()

#Items for Frisbee
category6 = Category(name = "Frisebe")
session.add(category6)
session.commit()

#Items for Rock Climbing
category7 = Category(name = "Rock Climbing")
session.add(category7)
session.commit()

#Items for Fooseball
category8 = Category(name = "Fooseball")
session.add(category8)
session.commit()

#Items for Skating
category9 = Category(name = "Skating")
session.add(category9)
session.commit()

print "Initial data loaded!"
