from fastapi import Depends, FastAPI
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def greet():
    return "Wellcome to my server"

products = [
    Product(id = 1,name = "phone", description = "budget phone", price = 99, quantity = 10),
    Product(id = 2,name = "laptop", description =  "budget laptop", price = 94, quantity = 17),
    Product(id = 5,name = "pen", description = "writes on notebook", price = 5, quantity = 14),
    Product(id = 6,name = "pencil", description =  "writes on tab", price = 31, quantity = 7)
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # # db connection
    # db = SessionLocal()
    # # query
    # db.query()
    db_products = db.query(database_models.Product).all()

    return  db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product Added successfully"

    return "Product not found"


@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted"
    return "product not found"
