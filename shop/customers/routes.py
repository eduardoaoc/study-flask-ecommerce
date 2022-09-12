from flask import redirect, render_template, url_for, flash, request, session, current_app
import secrets, os 

from shop import db, app, photos, products, search
from shop.admin.routes import category
from .forms import CustomerRegisterForm


def customer_register():
    return render_template('customer/register.html')
