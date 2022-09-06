from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, AddProduct
from .forms import Addproducts
import secrets, os 

@app.route('/home')
def home():
    return''

#adiciona uma marca
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    '''if 'email' not in session:
        flash(f'Please login first', 'danger')'''
    if request.method== 'POST':
        getbrand= request.form.get('brand')
        brand= Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands' )

#atualiza uma marca selecionada
@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    '''if 'email' not in session:
        flash(f'Please login first', 'danger')'''

    updatebrand= Brand.query.get_or_404(id) 
    brand= request.form.get('brand')

    if request.method == 'POST':
        updatebrand.name= brand
        flash(f'Your brand has been updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update brandy page', updatebrand=updatebrand)            

#remove uma marca
@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand= Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database.', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cant be deleted','warning')
    return redirect(url_for('admin'))

#adiciona uma categoria
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    '''if 'email' not in session:
        flash(f'Please login first', 'danger')'''

    if request.method== 'POST':
        getcat= request.form.get('category')
        cat= Category(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')    

#atualiza uma categoria selecionada
@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    '''if 'email' not in session:
        flash(f'Please login first', 'danger')'''

    updatecat= Category.query.get_or_404(id)
    category= request.form.get('category')

    if request.method == 'POST':
        updatecat.name= category
        flash(f'Your category has been updated','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update category page', updatecat=updatecat)            

#adiciona um produto
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    '''if 'email' not in session:
        flash(f'Please login first', 'danger')'''

    brands= Brand.query.all()
    categories= Category.query.all()
    form= Addproducts(request.form)

    if request.method =='POST':
        name= form.name.data
        price= form.price.data
        discount= form.discount.data
        stock= form.stock.data
        colors= form.colors.data
        desc= form.discription.data
        brand= request.form.get('brand')
        category= request.form.get('category')

        image_1=photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2=photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3=photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')

        addpro= AddProduct(name=name,price=price,discount=discount, stock=stock, colors=colors, desc=desc, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html' , title='Add product page', form=form, brands=brands, categories= categories)    

#atualiza o produto selicionado
@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands= Brand.query.all()
    categories= Category.query.all()
    product= AddProduct.query.get_or_404(id)
    brand= request.form.get('brand')
    category= request.form.get('category')
    form= Addproducts(request.form)

    if request.method == 'POST':
        product.name= form.name.data
        product.price= form.price.data
        product.discount= form.discount.data
        product.brand_id= brand
        product.category_id= category
        product.colors= form.colors.data
        product.desc= form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))  
                product.image_1=  photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')  
            except:
                product.image_1=  photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')  
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))  
                product.image_1=  photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')  
            except:
                product.image_1=  photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')  

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))  
                product.image_1=  photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')  
            except:
                product.image_1=  photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')  

        db.session.commit()
        flash(f'You product has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data= product.name
    form.price.data= product.price
    form.discount.data= product.discount
    form.stock.data= product.stock
    form.colors.data= product.colors
    form.discription.data= product.desc 
    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)
