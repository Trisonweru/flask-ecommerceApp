from flask import redirect, render_template, url_for, flash, request
from shop import app, db, photos

from .models import Brand, Category,AddProduct
from .forms import AddProducts

#hash our images
import secrets

@app.route("/", methods=['GET', 'POST'])
def home():
    products=AddProduct.query.filter(AddProduct.stock > 0) #check if the stock of the product is greater than 0 and display the products available to homepage.
    return render_template('products/index.html', products=products)
#responsble fro the details view of a product
@app.route("/detailspage/<int:id>", methods=["GET", "POST"])
def detailspage(id):
    product=AddProduct.query.get_or_404(id) #get the product with the id from the the request and pass in the product to the template for display.
    return render_template("products/detailspage.html", product=product)

#adding a product brand to database
@app.route("/addbrand", methods=['GET', 'POST'])
def addbrand():#if request method is post, the the form data and add to brand table
    if request.method=="POST":
        getbrand=request.form.get("brand")
        brand=Brand(name=getbrand)
        db.session.add(brand)
        flash(f"The brand {getbrand} was added succesfully.", "success")
        db.session.commit()
        return redirect(url_for("addbrand"))

    return render_template("products/addbrand.html", brands="brands")
#adding a product category to database
@app.route("/addcategory", methods=['GET', 'POST'])
def addcategory():
    if request.method=="POST": #if request method is post, the the form data and add to category table
        getcategory=request.form.get("category")
        category=Category(name=getcategory)
        db.session.add(category)
        flash(f"The category {getcategory} was added succesfully.", "success")
        db.session.commit()
        return redirect(url_for("addcategory"))

    return render_template("products/addbrand.html")
#responsible for adding a product to the database
@app.route("/addproduct", methods=['GET', 'POST'])
def addproduct():
    #getting brands categories
    brands=Brand.query.all()
    categories=Category.query.all()
    form=AddProducts(request.form) #instace of the form class to add products
    if request.method=="POST": #if the request is post, get the fields data and store it into respective varables
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        location=form.location.data
        desc=form.description.data
        colors=form.colors.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        image_1=photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2=photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3=photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        #add the prodcuts data to the addproduct table in the database
        add_products=AddProduct(name=name, price=price, discount=discount, stock=stock,
        location=location, description=desc, colors=colors, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        flash(f"The product {name} was added succesfully.", "success")
        db.session.add(add_products)
        db.session.commit() #commits the changes
        return redirect(url_for("admin"))
    return render_template("products/addproduct.html", title="Add product page", form=form, brands=brands, categories=categories)

#creating a route to update the products
@app.route("/updateproduct/<int:id>", methods=['GET', 'POST'])
def updateproduct(id):
    brand=Brand.query.all() #get all the brands from db
    category=Category.query.all()  #get all the categories from db
    product=AddProduct.query.get_or_404(id) #get the product with the requested id
    brand=request.form.get('brand') 
    category=request.form.get('category')
    form=AddProducts(request.form)
    #getting data from our Addproducts form
    if request.method == "POST": 
        product.name=form.name.data
        product.price=form.price.data
        product.description=form.description.data
        product.location=form.location.data
        product.stock=form.stock.data
        product.colors=form.colors.data
        product.discount=form.discount.data
        product.brand_id=brand
        product.category_id=category     
        db.session.commit()
        flash(f"The product {product.name} was updated succesfully.", "success")
        return redirect(url_for('admin'))
#setting the fields in the form to their respective values stored in the database
    form.name.data=product.name
    form.price.data=product.price
    form.description.data=product.description
    form.location.data=product.location
    form.stock.data=product.stock
    form.colors.data=product.colors
    form.discount.data=product.discount
    
    return render_template("products/updateproduct.html", form=form, category=category, brand=brand, product=product)
#responsible for deleting a product from the admin dashboard
@app.route("/deleteproduct/<int:id>", methods=["GET","POST"])
def deleteproduct(id):
    product=AddProduct.query.get_or_404(id)#check the product with the id passed with the request
    if request.method=="POST": #if the product exist, we would like to delete the product from our seesion
        db.session.delete(product)
        db.session.commit()
        flash(f"The product {product.name} was deleted succesfully.", "success")
        return redirect(url_for("admin"))
    flash(f"The product {product.name} could not be deleted.", "danger")