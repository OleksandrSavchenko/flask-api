import models
from app import db
import uuid

# db.create_all()
#
# user = User('test', 'test@gmail.com', '12345678')
#
# db.session.add(user)
# db.session.commit()

customer = models.Customer(public_id=str(uuid.uuid4()), name='Rik Morty', address='Ukraine, Kyiv, Soloma str., 234', phone='+380989694355')
customer1 = models.Customer(public_id=str(uuid.uuid4()), name='Erik Kirk', address='USA, NY, Blabla str., 123d', phone='+190989694355')
customer2 = models.Customer(public_id=str(uuid.uuid4()), name='Megan Fox', address='England, Barber str., 24a', phone='+280989694355')

db.session.add(customer)
db.session.add(customer1)
db.session.add(customer2)
db.session.commit()

product = models.Product(public_id=str(uuid.uuid4()), name='Telephone', price=123)
product1 = models.Product(public_id=str(uuid.uuid4()), name='TV', price=466)
product2 = models.Product(public_id=str(uuid.uuid4()), name='MacBook', price=1200)

db.session.add(product)
db.session.add(product1)
db.session.add(product2)
db.session.commit()



