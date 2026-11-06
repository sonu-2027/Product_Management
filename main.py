from fastapi import FastAPI
from models import Product
from database import Session

app=FastAPI()

@app.get('/')
def greet():
  return "hii"

products = [
    Product(id=1,name="phone",desc="budget phone",price=99,quantity=50),
    Product(id=2,name="laptop",desc="a powerful laptop",price=999.99,quantity=30),
    Product(id=3,name="pen",desc="a blue ink",price=1.99,quantity=100),
    Product(id=4,name="table",desc="a woonden table",price=199.99,quantity=20)
]

@app.get("/products")
def get_all_products():
  db = Session()
  return products

@app.get("/product{id}")
def get_product_by_id(id:int):
  for product in products:
    if product.id == id:
      return product
    
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