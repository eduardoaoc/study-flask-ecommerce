from unicodedata import category
from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app
from .models import Brand, Category, AddProduct
from .forms import Addproducts
import secrets

@app.route('/')
def gome():
    return''

#adiciona e atualiza marca  
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    if request.method== 'POST':
        getbrand= request.form.get('brand')
        brand= Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands' )



@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatebrand= Brand.query.get_or_404(id) 
    brand= request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name= brand
        flash(f'Your brand has been updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update brandy page', updatebrand=updatebrand)            


#adiciona e atualiza categoria
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    if request.method== 'POST':
        getcat= request.form.get('category')
        cat= Brand(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')    


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatcat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatecat= Category.query.get_or_404(id)
    category= request.form.get('category')
    if request.method == 'POST':
        updatecat.name= category
        flash(f'Your category has been updated','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update category page', updatecat=updatecat)            

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    form= Addproducts(request.form)
    return render_template('products/addproduct.html' , title='Add product page', form=form)    