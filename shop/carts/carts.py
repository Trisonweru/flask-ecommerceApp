# The codes below is responsible for what goes on in the carts page
from flask import redirect, render_template, url_for, flash, request,session
from shop import app, db #
from shop.products.models import AddProduct
from decimal import Decimal
from shop.customers.models import Customer
from shop.reseller.models import Reseller
#from shop.admin.models import Order
from shop.products.models import CustomerOrder
import stripe
import secrets

#publishable key from stripe
publishable_key="pk_test_51Hb7T9LEdnNAm34FNAN277FHhXQb0kXtTD8sKUmKyfe9DM5QvDAhxRYRXOCffV1705ou7YveDaZtCK3Mt8QJQ24I00qmOyFPuE"
#secret key from stripe
stripe.api_key="sk_test_51Hb7T9LEdnNAm34FM39TocpnPkcAMBt3NrFBIWpnDqsNSpQyu1sXONXIo5AboR0zPUUKrzgAo8xtZ4cvYM2H1WLm007wTlsrpO"

#payment with stripe integration
@app.route("/payment", methods=["POST"]) # when user hits the payment button with stripe, the following function is executed
def payment():
    subtotal=0
    total=0
    for key, product in session['ShoppingCart'].items(): #getting our cart items an calculating the subtotal for each and evetually calculates the cart total
        discount=(product['discount']/100)*float(product['price'])
        subtotal += float(product['price'])*int(product['quantity'])
        subtotal -= discount
        total=float("%.2f" % (subtotal))
    customer = stripe.Customer.create(email=request.form['stripeEmail'],source=request.form['stripeToken'],)# creating a customer in stripe and passing their email and the source
    charge = stripe.Charge.create(customer=customer.id, description='Test payment', amount=int(total), currency='usd',)# creating a charge for the customer to be deducted from their account
    #once the charge has been made, we would like to change the order status to paid
    #so we query the user that paid 
    email=session['email'] # this user has their email in session
    user_details=None
    #checks what kind of user either reseller or customer and set their details touser details variable above
    if Customer.query.filter_by(email=email).first():
        user_details=Customer.query.filter_by(email=email).first()
    elif Reseller.query.filter_by(email=email).first():
        user_details = Reseller.query.filter_by(email=email).first()
    else:
        user_details=None
        return redirect(url_for('login'))
    customer_id=user_details.id # gtting the id of the logged in user
    orders=CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first() #getting their recent order
    orders.status="Paid" # changing the order status to paid
    return redirect(url_for('thankyou')) # then display a thank you page
#route to the thank you page
@app.route("/thankyou", methods=['POST', 'GET'])
def thankyou():
   return render_template("products/thankyou.html")

#merging shopping cart dictionaries for multiple orders
def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list): # check if the instaces are lists i so, we concatenate them
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict): #else if the instaces are dictionaries we also concatenate them and form a single distionary
        return dict(list(dict1.items())+list(dict2.items())) #returns the concatenated dictionary with all items
    return False
# add item to cart whn user clicks add to cart
@app.route('/addcart', methods=["POST", "GET"])
def AddCart():
    try:
        product_id=request.form.get("product_id")
        quantity=request.form.get("quantity")
        colors=request.form.get("colors")
        product=AddProduct.query.filter_by(id=product_id).first()

        if product_id and quantity and colors and request.method=="POST":
            dict_items={product_id:{"name": product.name, "price":Decimal(product.price), "discount":product.discount, "colors":colors, "quantity":quantity, "image":product.image_1}} #creating a dictionary to hold the cart items
            if 'ShoppingCart'in session: #checks if the entered item is already in cart session
                print(session['ShoppingCart'])
                if product_id in session['ShoppingCart']:
                    flash(f"This product is already in your cart.", "warning")
                    #print("This product is already in your cart")
                else: #if the cart item is not in session we use our mergedict function to concatenate to the alredy existing cart in session with the new dict item
                    session['ShoppingCart']=MergeDicts(session['ShoppingCart'], dict_items)
                    return redirect(request.referrer) #return back to the same request page
            else:
                session['ShoppingCart']=dict_items # if we dont have cart at all then add the cart in session 
                return redirect(request.referrer)# and return to the same request page.
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

#reponsible for displaying cart items
@app.route("/carts", methods=['POST', 'GET'])
def cart():
    if 'ShoppingCart' not in session or len(session['ShoppingCart'])<=0: #check the length of cart if is greater than 0 then proceed to cart otherwise return to the same request page.
        return redirect(url_for(request.referrer)) # we only would like to display cart if we have items in the cart
    subtotal=0
    total=0
    for key, product in session['ShoppingCart'].items(): #if we have a cart, we iterate through the elements of the cart and calculate subtotal and total of th cart and and pass to our template for display 
        discount=(product['discount']/100)*float(product['price'])
        subtotal += float(product['price'])*int(product['quantity'])
        subtotal -= discount
        total=float("%.2f" % (subtotal))
    return render_template("products/carts.html", total=total)

#delete item route
@app.route("/deleteitem/<int:id>", methods=["POST", "GET"])
def deleteitem(id):
    if 'ShoppingCart' not in session or len(session['ShoppingCart'])<=0: #check the length of the cart if 0 we go back home, this is our base case
        return redirect(url_for("home"))
    #else we try to modify the session and pop the distionary key fro the cart in session with th same id clicked.
    try:
        session.modified=True
        for key, product in session['ShoppingCart'].items():
            if int(key)==id:
                session['ShoppingCart'].pop(key, None)
                return redirect(url_for("home"))
    except Exception as e:
        print(e)
        return redirect(url_for("cart"))
#proceed to checkout route
@app.route("/checkout", methods=["POST", "GET"])
def checkout():
    if 'email' not in session: #checks if the email is in session to acces this route
        flash(f'Please login to access this route.', 'danger')
        return redirect(url_for('login'))
    elif 'ShoppingCart' not in session or len(session['ShoppingCart'])<=0:
        return redirect(url_for("home"))
    subtotal=0
    total=0
    #if the cart is in session, get the cart total and pass it to the template
    for key, product in session['ShoppingCart'].items():
        discount=(product['discount']/100)*float(product['price'])
        subtotal += float(product['price'])*int(product['quantity'])
        subtotal -= discount
        total=float("%.2f" % (subtotal))
    #get what user is logged in either customer or reseller and pass it to our template
    email=session['email']
    user=""
    user_details=None
    if Customer.query.filter_by(email=email).first():
        user="customer"
        user_details=Customer.query.filter_by(email=email).first()
    elif Reseller.query.filter_by(email=email).first():
        user="reseller"
        user_details=Reseller.query.filter_by(email=email).first()
    else:
        user=""
        user_details=None
        return redirect(url_for('login'))
     #defining a list of shipping methods, if user is customer, they see the full list otherwise the user is a resseller and they see the other two except in house method   
    shipping_method=["In-house", "DHL", "B2B Europe"]
    products=[session['ShoppingCart']]
    print(products)
    return render_template("products/checkout.html", total=total, user=user, user_details=user_details, shipping_method=shipping_method)

# a route to insert an order to the database when proeed to checkout button is clicked
@app.route('/orders')
def orders():
    if 'email' not in session: #checks if their is an email in seesion to access this route
        flash(f'Please login to access this route.', 'danger')
        return redirect(url_for('login'))
    #getting the logged in user details
    email=session['email']
    user_details=None
    if Customer.query.filter_by(email=email).first():
        user_details=Customer.query.filter_by(email=email).first()
    elif Reseller.query.filter_by(email=email).first():
        user_details = Reseller.query.filter_by(email=email).first()
    else:
        user_details=None
        return redirect(url_for('login'))
    #setting the logged in user id to customer id
    customer_id=user_details.id
    invoice=secrets.token_hex(5) #create a random invoice mumber
    try:
        #publish the order to our database with the invoice, customer_id and the orders object
        order=CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['ShoppingCart'])
        db.session.add(order)
        db.session.commit()
        flash('Your order is pending', "success")
        return redirect(url_for('checkout'))        
    except Exception as e:
        print(e)
        flash("Something went wrong", "danger")
        return redirect(url_for('home'))
    return render_template("products/orders.html")

    


