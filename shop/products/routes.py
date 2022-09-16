from flask import redirect, render_template, url_for, flash, request, session, current_app
import secrets, os 

from shop import db, app, photos, products, search
from shop.admin.routes import category
from .models import Brand, Category, AddProduct
from .forms import Addproducts


#página inicial/ todos produtos
@app.route('/')
def home():
    page= request.args.get('page', 1, type=int)
    products= AddProduct.query.filter(AddProduct.stock > 0).order_by(AddProduct.id.desc()).paginate(page=page, per_page= 8)
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    brands= Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)

#pequisa de produtos, etc.
@app.route('/result')
def result():
    searchword= request.args.get('q')
    products= AddProduct.query.msearch(searchword, fields=['name', 'desc'], limit=6)
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    brands= Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    return render_template('products/result.html', products=products, brands=brands, categories=categories)


#página individual de um produto
@app.route('/product/<int:id>')
def single_page(id):
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    brands= Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    product= AddProduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, brands=brands, categories=categories)

#página de produtos por marca
@app.route('/brand/<int:id>')
def get_brand(id):
    page= request.args.get('page', 1, type=int)
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    get_b= Brand.query.filter_by(id=id).first_or_404()
    brand= AddProduct.query.filter_by(brand=get_b).paginate(page=page, per_page=6)
    brands= Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories, get_b=get_b)

#página de produtos por categoria
@app.route('/categories/<int:id>')
def get_category(id):
    page= request.args.get('page', 1, type=int)
    get_cat= Category.query.filter_by(id=id).first_or_404()
    get_cat_prod= AddProduct.query.filter_by(category=get_cat).paginate(page=page, per_page= 6)
    brands= Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories, brands=brands, get_cat=get_cat)

#adiciona uma marca
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method== 'POST':
        getbrand= request.form.get('brand')
        brand= Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database.', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands' )

#atualiza uma marca selecionada
@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
    updatebrand= Brand.query.get_or_404(id) 
    brand= request.form.get('brand')

    if request.method== 'POST':
        updatebrand.name= brand
        flash(f'Your brand has been updated.','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update brandy page', updatebrand=updatebrand)            

#remove uma marca
@app.route('/deletebrand/<int:id>')
def deletebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
    brand= Brand.query.filter_by(id=id).first()
    try:
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database.', 'success')
    except:
        flash(f'An error ocurred','danger')    
    return redirect(url_for('brands'))
  
#adiciona uma categoria
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
    if request.method== 'POST':
        getcat= request.form.get('category')
        cat= Category(name=getcat)
        db.session.add(cat)
        flash(f'The category {getcat} was added to your database.', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')    

#atualiza uma categoria selecionada
@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
    updatecat= Category.query.get_or_404(id)
    category= request.form.get('category')

    if request.method== 'POST':
        updatecat.name= category
        flash(f'Your category has been updated.','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update category page', updatecat=updatecat)            

#remove uma categoria
@app.route('/deletecat/<int:id>')
def deletecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
    category= Category.query.filter_by(id=id).first()
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database.', 'success')
    except:
        flash(f'An error ocurred','danger')    
    return redirect(url_for('category'))
  
#adiciona um produto
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
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

        addpro= AddProduct(name=name,price=price,discount=discount, stock=stock, colors=colors, 
        desc=desc, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database.', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html' , title='Add product page', form=form, brands=brands, categories= categories)    

#atualiza o produto selicionado
@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
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
        flash(f'You product has been updated.', 'success')
        return redirect(url_for('admin'))

    form.name.data= product.name
    form.price.data= product.price
    form.discount.data= product.discount
    form.stock.data= product.stock
    form.colors.data= product.colors
    form.discription.data= product.desc 
    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

#remove um produto
@app.route('/deleteproduct/<int:id>')
def deleteproduct(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
        
    product= AddProduct.query.filter_by(id=id).first()
    try:
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))  
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))  
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))  
    except Exception as e:
        print(e)
        flash(f'An error ocurred.','danger')    
    db.session.delete(product)
    db.session.commit()
    flash(f'The product {product.name} was deleted from your database.', 'success')
    return redirect(url_for('admin'))
   