from models import *
from app import db

db.create_all()

customer = Customer('Rik Morty', 'Ukraine, Kyiv, Soloma str., 234', '+380989694355')
customer1 = Customer('Erik Kirk', 'USA, NY, Blabla str., 123d', '+190989694355')
customer2 = Customer('Megan Fox', 'England, Barber str., 24a', '+280989694355')

db.session.add(customer)
db.session.commit()
db.session.add(customer1)
db.session.commit()
db.session.add(customer2)
db.session.commit()

product = Product('Telephone', 123)
product1 = Product('TV', 466)
product2 = Product('MacBook', 1200)

db.session.add(product)
db.session.commit()
db.session.add(product1)
db.session.commit()
db.session.add(product2)
db.session.commit()



