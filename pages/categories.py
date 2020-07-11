import json

from flask import Flask, render_template, redirect, url_for, Blueprint

from utils.ishtarManager import IshtarManager
from utils.flatten import flattenClass

manager = IshtarManager('./data/EncryptedIshtarData.pickle')

categories = Blueprint('categories', __name__, template_folder='./templates')

@categories.route('')
def show_categories():
    return render_template(
        'categories.html',
        title = 'Hero\'s Lore | Search Categories',
        categories = manager.categories
    )
