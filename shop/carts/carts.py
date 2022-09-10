from traceback import print_tb
from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import AddProduct
from shop.products.routes import *


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


#metodo para adicionar um produto ao carrinho
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = AddProduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method=='POST':
            DictItems = {product_id: {'name': product.name, 'price':product.price, 'discount': product.discount, 'color': product.colors, 
            'quantity': quantity, 'image': product.image_1, 'colors': product.colors}}
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:
                    for key , item in session['Shoppingcart'].items():
                        print(key, item)
                        if int(key) == int(product_id):
                            session.modified = True 
                            qnt = int(item['quantity'])
                            qnt +=1
                            item['quantity'] = qnt
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

#página do carrinho de compras 
@app.route('/carts')
def getCart():
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    brands= Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal=0
    total=2    
    for key , product in session['Shoppingcart'].items():
        discount= (product['discount']/100) * float(product['price'])
        subtotal+= float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax= ("%.2f" % (.06 * float(subtotal)))
        total= float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html', tax=tax, total=total, categories=categories, brands=brands)    