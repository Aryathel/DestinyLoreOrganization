import json
from math import ceil

from flask import Flask, render_template, redirect, url_for, Blueprint, request

from utils.ishtarManager import IshtarManager
from utils.flatten import flattenClass

manager = IshtarManager('./data/EncryptedIshtarData.pickle')

loreEntries = Blueprint('loreEntries', __name__, template_folder='./templates')

@loreEntries.route('')
def show_entries():
    page = int(request.args.get('page', 1))
    name = request.args.get('name', None)
    if name:
        named_cards = manager.loadLoreEntriesByName(name)
        adjusted_cards = [[]]
        i = 0
        for card in named_cards:
            if len(adjusted_cards[i]) > 1:
                adjusted_cards.append([])
                i += 1
            adjusted_cards[i].append(card)
        card_set = adjusted_cards
        num_pages = ceil(len(named_cards)/16)
    else:
        num_pages = ceil(len(manager.loreEntries)/16)
        adjusted_cards = [[]]
        i = 0
        for card in manager.loreEntries:
            if card.fullImageUrl == "":
                for category in card.categories:
                    print(category.hashName)
            if len(adjusted_cards[i]) > 1:
                adjusted_cards.append([])
                i += 1
            adjusted_cards[i].append(card)

        card_set = adjusted_cards[(page - 1) * 9 - (page - 1):(page * 9) - page]
    return render_template(
        'loreEntries.html',
        title = 'Hero\'s Lore | Search Lore Entries',
        cards = card_set,
        raw_entries = manager.loreEntries,
        page = page,
        num_pages = num_pages
    )
