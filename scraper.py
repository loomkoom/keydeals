import cheapkeys
import g2a
import humble
import plati
import json


def get_data(store):
    if store == 'plati':
        return plati.fetch()
    if store == 'g2a':
        return g2a.fetch()
    if store == 'humble':
        return humble.fetch()
    if store == 'cheapkeys':
        return cheapkeys.fetch()

