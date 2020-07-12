import sys

from flask import Flask, redirect, url_for, render_template

from utils.ishtarManager import IshtarManager

manager = IshtarManager('./data/EncryptedIshtarData.pickle')

if "--web" in sys.argv:
    from pages.categories import categories
    from pages.grimoireCards import cards
    from pages.items import items
    from pages.loreEntries import loreEntries

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
else:
    lore = manager.buildCollections()
    char_count = 0
    word_count = 0
    for era in lore.keys():
        print(era)
        char_count += len(era)
        word_count += len(era.split(' '))
        if 'books' in lore[era].keys():
            for book in lore[era]['books'].keys():
                print("  " + book)
                char_count += len(book)
                word_count += len(book.split(' '))
                for chapter in lore[era]['books'][book]:
                    char_count += len(chapter.description)
                    word_count += len(chapter.description.split(' '))
        elif 'cards' in lore[era].keys():
            for card in lore[era]['cards']:
                char_count += len(card.description)
                word_count += len(card.description.split(' '))
            if era == "The Taken King":
                print("  Books of Sorrow")
            elif era == "House of Wolves":
                print("  The Maraid")

    print(f"Rough lore book character count: {char_count}")
    print(f"Rough lore book word count: {word_count}")
