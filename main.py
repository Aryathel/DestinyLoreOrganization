from flask import Flask, redirect, url_for, render_template

from utils.ishtarManager import IshtarManager

from pages.categories import categories
from pages.grimoireCards import cards
from pages.items import items
from pages.loreEntries import loreEntries

manager = IshtarManager('./data/EncryptedIshtarData.pickle')

app = Flask(__name__)
app.register_blueprint(categories, url_prefix='/categories')
app.register_blueprint(cards, url_prefix='/grimoire-cards')
app.register_blueprint(items, url_prefix="/items")
app.register_blueprint(loreEntries, url_prefix="/lore-entries")

@app.route('/')
def index():
    return render_template(
        'index.html',
        title = "Hero's Lore | Home"
    )

app.run("localhost", port = 7777, debug = True)
