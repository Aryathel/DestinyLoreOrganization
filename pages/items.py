import json
from math import ceil

from flask import Flask, render_template, redirect, url_for, Blueprint, request

from utils.ishtarManager import IshtarManager
from utils.flatten import flattenClass

manager = IshtarManager('./data/EncryptedIshtarData.pickle')

items = Blueprint('items', __name__, template_folder='./templates')

@items.route('')
def show_items():
    page = int(request.args.get('page', 1))
    name = request.args.get('name', None)
    if name:
        named_items = manager.loadItemsByName(name)
        adjusted_items = [[]]
        i = 0
        for item in named_items:
            if len(adjusted_items[i]) > 3:
                adjusted_items.append([])
                i += 1
            adjusted_items[i].append(item)
        item_set = adjusted_items
        num_pages = ceil(len(named_items) / 16)
    else:
        num_pages = ceil(len(manager.items)/16)
        adjusted_items = [[]]
        i = 0
        for item in manager.items:
            if len(adjusted_items[i]) > 3:
                adjusted_items.append([])
                i += 1
            adjusted_items[i].append(item)

        item_set = adjusted_items[(page - 1) * 5 - (page - 1):(page * 5) - page]
    return render_template(
        'items.html',
        title = 'Hero\'s Lore | Search Items',
        items = item_set,
        raw_items = manager.items,
        page = page,
        num_pages = num_pages
    )
