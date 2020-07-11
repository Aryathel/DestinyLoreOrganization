import json
from math import ceil

from flask import Flask, render_template, redirect, url_for, Blueprint, request

from utils.ishtarManager import IshtarManager
from utils.flatten import flattenClass

manager = IshtarManager('./data/EncryptedIshtarData.pickle')

cards = Blueprint('cards', __name__, template_folder='./templates')

@cards.route('')
def show_grimoire_cards():
    page = int(request.args.get('page', 1))
    name = request.args.get('name', None)
    if name:
        named_cards = manager.loadGrimoireByName(name)
        adjusted_cards = [[]]
        i = 0
        for card in named_cards:
            if len(adjusted_cards[i]) > 3:
                adjusted_cards.append([])
                i += 1
            adjusted_cards[i].append(card)
        card_set = adjusted_cards
        num_pages = ceil(len(named_cards)/16)
    else:
        num_pages = ceil(len(manager.grimoireCards)/16)
        adjusted_cards = [[]]
        i = 0
        for card in manager.grimoireCards:
            if len(adjusted_cards[i]) > 3:
                adjusted_cards.append([])
                i += 1
            adjusted_cards[i].append(card)

        card_set = adjusted_cards[(page - 1) * 5 - (page - 1):(page * 5) - page]
    return render_template(
        'grimoireCards.html',
        title = 'Hero\'s Lore | Search Grimoire Cards',
        cards = card_set,
        raw_cards = manager.grimoireCards,
        page = page,
        num_pages = num_pages
    )
