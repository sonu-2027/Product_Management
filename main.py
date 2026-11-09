from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
import db_models
from sqlalchemy.orm import Session

app=FastAPI()

db_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
  return "hii"

products = [
    Product(id=1,name="phone",desc="budget phone",price=99,quantity=50),
    Product(id=2,name="laptop",desc="a powerful laptop",price=999.99,quantity=30),
    Product(id=3,name="pen",desc="a blue ink",price=1.99,quantity=100),
    Product(id=4,name="table",desc="a woonden table",price=199.99,quantity=20)
]

def get_db():
  db = session()
  try:
    yield db
  finally:
    db.close()


def init_db():
  db = session()
  count = db.query(db_models.Product).count()

  if count == 0:
    for product in products:
      db.add(db_models.Product(**product.model_dump()))
    db.commit()
init_db()


@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):

  db_products = db.query(db_models.Product).all()
  return db_products

@app.get("/product{id}")
def get_product_by_id(id:int,db:Session = Depends(get_db)):
  db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
  if db_product:
    return db_product
  return "Product not found"

@app.post("/product")
def add_product(product: Product):
  products.append(product)
  return product

@app.put("/product")
def update_product(id:int,product:Product):
  for i in range(len(products)):
    if products[i].id == id:
      products[i] = product
      return "prod added succeessfully"
  return "prod not ava"

@app.delete("/product")
def delete_product(id:int,product:Product):
  for i in range(len(products)):
    if products[i].id == id:
      del products[i]
      return "prod deleted succeessfully"
  return "prod not ava"