import os
from enum import Enum
import pickle
import difflib
import json
import roman
import html

import requests

from utils.progressBar import ProgressBar
from data.collectionsList import LORE_BOOK_COLLECTIONS, CHAPTERS

class Category:
    def __init__(self, data):
        self.hashName = data.get('ishtar_ref')
        self.name = data.get('name')
        self.ishtarUrl = data.get('ishtar_url')
        self.apiUrl = data.get('api_url')
        self.shortSummary = data.get('short_summary')
        self.summary = data.get('summary', None)
        self.plainTextSummary = data.get('plain_text_summary', None)
        self.featured = data.get('featured', None)
        self.chronological = data.get('chronological', None)
        self.count = data.get('count', None)

class GrimoireCard:
    def __init__(self, data):
        self.hashName = data.get('ishtar_ref')
        self.name = data.get('name')
        self.ishtarUrl = data.get('ishtar_url')
        self.apiUrl = data.get('api_url')
        self.shortSummary = data.get('short_summary')
        self.bungieRef = data.get('bungieRef')
        self.imageUrl = data.get('image_url')
        self.fullImageUrl = data.get('full_image_url')
        self.intro = data.get('intro')
        self.introAttribution = data.get('intro_attribution')
        self.description = html.unescape(data.get('description')).replace('<br/>', '\n') if data.get('description') else None
        self.bungieDeleted = data.get('bungie_deleted')
        if data.get('categories'):
            self.categories = [Category(i) for i in data.get('categories')]
        else:
            self.categories = []

class Item:
    def __init__(self, data):
        self.hashName = data.get('ishtar_ref')
        self.name = data.get('name')
        self.ishtarUrl = data.get('ishtar_url')
        self.apiUrl = data.get('api_url')
        self.shortSummary = data.get('short_summary')
        self.bungieRef = data.get('bungie_ref')
        self.imageUrl = data.get('image_url')
        self.fullImageUrl = data.get('full_image_url')
        self.displaySource = data.get('display_source')
        self.description = html.unescape(data.get('description')).replace('<br/>', '\n') if data.get('description') else None
        self.bungieDeleted = data.get('bungie_deleted')
        if data.get('categories'):
            self.categories = [Category(i) for i in data.get('categories')]
        else:
            self.categories = []

class LoreEntry:
    def __init__(self, data):
        self.hashName = data.get('ishtar_ref')
        self.name = data.get('name')
        self.ishtarUrl = data.get('ishtar_url')
        self.apiUrl = data.get('api_url')
        self.shortSummary = data.get('short_summary')
        self.bungieRef = data.get('bungie_ref')
        self.imageUrl = data.get('image_url')
        self.fullImageUrl = data.get('full_image_url')
        if self.fullImageUrl == '':
            self.fullImageUrl = "./static/missing_entry.png"
        self.subtitle = data.get('subtitle')
        self.description = html.unescape(data.get('description')).replace('<br/>', '\n') if data.get('description') else None
        self.bungieDeleted = data.get('bungie_deleted')
        if data.get('categories'):
            self.categories = [Category(i) for i in data.get('categories')]
        else:
            self.categories = []
        if data.get('items'):
            self.items = [Item(i) for i in data.get('items')]
        else:
            self.items = []

class Transcript:
    def __init__(self, data):
        self.hashName = data.get('ishtar_ref')
        self.name = data.get('name')
        self.ishtarUrl = data.get('ishtar_url')
        self.apiUrl = data.get('api_url')
        self.shortSummary = data.get('short_summary')

class Record:
    def __init__(self, data):
        self.hashName = data.get('ishtar_ref')
        self.name = data.get('name')
        self.ishtarUrl = data.get('ishtar_url')
        self.apiUrl = data.get('api_url')
        self.shortSummary = data.get('short_summary')
        self.bungieRef = data.get('bungie_ref')
        self.imageUrl = data.get('image_url')
        self.fullImageUrl = data.get('full_image_url')
        self.description = html.unescape(data.get('description')).replace('<br/>', '\n') if data.get('description') else None
        if data.get('categories'):
            self.categories = [Category(i) for i in data.get('categories')]
        else:
            self.categories = []

class IshtarManager:
    ISHTAR_ROOT = 'https://api.ishtar-collective.net/'
    BUNGIE_ROOT = 'https://www.bungie.net/'
    BUNGIE_API_EXT = '/Platform'

    class Collection(Enum):
        categories = "categories"
        grimoire_cards = "cards"
        items = "items"
        entries = "entries"
        transcripts = "transcripts"
        records = "records"

    def __init__(self, dataFileLoc):
        self.dataFileLoc = os.path.abspath(dataFileLoc)
        self.path = os.path.dirname(self.dataFileLoc)
        self._session = requests.Session()

        self.LORE_BOOK_COLLECTIONS = LORE_BOOK_COLLECTIONS
        self.CHAPTERS = CHAPTERS

        if not os.path.isfile(self.dataFileLoc):
            self.updateCollective()
        self.loadCollective()

    def loadCollective(self):
        with open(self.dataFileLoc, 'rb') as file:
            raw_data = pickle.load(file)
        for key in raw_data.keys():
            if len(raw_data[key]) == 0:
                continue
            if self.Collection(key) == self.Collection.categories:
                self.categories = [Category(j) for j in raw_data[key]]
            elif self.Collection(key) == self.Collection.grimoire_cards:
                self.grimoireCards = [GrimoireCard(j) for j in raw_data[key]]
            elif self.Collection(key) == self.Collection.items:
                self.items = [Item(j) for j in raw_data[key]]
            elif self.Collection(key) == self.Collection.entries:
                self.loreEntries = [LoreEntry(j) for j in raw_data[key]]
            elif self.Collection(key) == self.Collection.transcripts:
                self.transcripts = [Transcript(j) for j in raw_data[key]]
            elif self.Collection(key) == self.Collection.records:
                self.records = [Record(j) for j in raw_data[key]]
        print('Loaded Collective')

    def updateCollective(self):
        res = self._session.get(self.ISHTAR_ROOT)
        if res.status_code == 200:
            routing = res.json()
            raw_data = {}
            for collection in routing['navigation'].keys():
                data = self._session.get(routing['navigation'][collection])
                if data.status_code == 200:
                    raw_data[collection] = []
                    response = data.json()
                    try:
                        collection_prop = self.Collection(collection)
                        pb = ProgressBar(' ', '█', response['meta']['total_count'])
                        pb.progress(0, status = 'Loading Ishtar ' + collection.capitalize())
                        while 'meta' in response.keys() and 'next_page' in response['meta'].keys() and response['meta']['next_page']:
                            for i in response[collection_prop.name]:
                                pb.progress(1, status = 'Loading Ishtar ' + collection.capitalize())
                                raw_data[collection].append(i)
                            data = self._session.get(response['meta']['next_page_url'])
                            if data.status_code == 200:
                                response = data.json()
                            else:
                                raise Exception(f"Failed to retrieve Ishtar Collective {collection} collection: {data.status_code}")
                            pb.ETA()
                        collection_prop = self.Collection(collection)
                        for i in response[collection_prop.name]:
                            pb.progress(1, status = 'Loading Ishtar ' + collection.capitalize())
                            raw_data[collection].append(i)
                    except:
                        pass

                else:
                    raise Exception(f"Failed to retrieve Ishtar Collective {collection} collection: {data.status_code}")
            with open(self.dataFileLoc, 'wb+') as file:
                pickle.dump(raw_data, file)
        else:
            raise Exception(f"Failed to retrieve Ishtar Collective routing: {res.status_code}")

    def buildCollections(self):
        collected = {}
        for card in self.grimoireCards:
            for category in card.categories:
                for collection in self.LORE_BOOK_COLLECTIONS["D1"].keys():
                    if not collection in collected.keys():
                        collected[collection] = {"cards": []}
                    for book in self.LORE_BOOK_COLLECTIONS["D1"][collection]:
                        if book.lower() in category.name.lower():
                            collected[collection]['cards'].append(card)

        for entry in self.loreEntries:
            for category in entry.categories:
                for collection in self.LORE_BOOK_COLLECTIONS["D2"].keys():
                    if not collection in collected.keys():
                        collected[collection] = {"books": {}}
                    for book in self.LORE_BOOK_COLLECTIONS["D2"][collection]:
                        if book.lower() in category.name.lower():
                            if not book in collected[collection]["books"].keys():
                                collected[collection]["books"][book] = []
                            collected[collection]["books"][book].append(entry)

        for entry in collected.keys():
            if 'cards' in collected[entry].keys():
                collected[entry]['cards'] = sorted(collected[entry]['cards'], key = self.sortD1Collection)
            elif 'books' in collected[entry].keys():
                collected[entry]['books'] = self.sortD2Books(collected[entry]['books'])

        return collected

    def sortD1Collection(self, x):
        x = x.name
        try:
            s = ':'.join(x.split(':')[1:])
            r = roman.fromRoman(x.split(':')[0])
        except:
            s = x
            if 'Curiosity' in s:
                r = 0
            elif 'Insight' in s:
                r = 200
            else:
                r = 0
        finally:
            return r, s

    def sortD2Books(self, books):
        res = {}
        for book in books.keys():
            res[book] = sorted(books[book], key = lambda x: self.CHAPTERS[book].index(x.name))
        return res

    def loadItemByName(self, name):
        name = difflib.get_close_matches(name, [item.name for item in self.items], n=1)
        if len(name) > 0:
            name = name[0]
        for item in self.items:
            if item.name == name:
                return item
        return None

    def loadItemsByName(self, name):
        names = difflib.get_close_matches(name, [item.name for item in self.items], n=16)
        for item in self.items:
            if item.name in names:
                names[names.index(item.name)] = item
        return names

    def loadGrimoireByName(self, name):
        names = difflib.get_close_matches(name, [card.name for card in self.grimoireCards], n=16)
        for card in self.grimoireCards:
            if card.name in names:
                names[names.index(card.name)] = card
        return names

    def loadLoreEntriesByName(self, name):
        names = difflib.get_close_matches(name, [entry.name for entry in self.loreEntries], n=16)
        for entry in self.loreEntries:
            if entry.name in names:
                names[names.index(entry.name)] = entry
        return names

if __name__ == "__main__":
    manager = IshtarManager('./data/EncryptedIshtarData.pickle')
    manager.buildCollections()
