import sublime
import sublime_plugin

try:
  from urllib.request import urlopen
  from urllib.parse import urlparse
  import urllib2
except ImportError:
  from urlparse import urlparse
  from urllib import urlopen

import json
import re

class BitcoinTicker(sublime_plugin.EventListener):

  def check_for_calc(self):
    """
      If enabled in settings, searches the view for a bitcoin amount to convert and
      replaces string with converted value.

      Supported formats that will be searched:
        1 BTC
        0.252 btc
        .5 btc
        13.303 BTC
    """

    settings = sublime.load_settings(__name__ + '.sublime-settings')
    convert_strings = settings.get('convert_strings')

    if convert_strings:
      regex = r'([-+]?[0-9]*\.?[0-9]+)\s*btc'
      extractions = []
      regions = self.view.find_all(regex, sublime.IGNORECASE, "$1", extractions)

      added_length = 0
      btc_in_usd, exchange_name = self.get_current_exchange()
      for index, region in enumerate(regions):
        amount = float(extractions[index])
        result = btc_in_usd * amount

        edit = self.view.begin_edit()
        added_length += self.view.insert(edit, region.end() + added_length, " => $%.2f (%s)" % (result, exchange_name))
        self.view.end_edit(edit)

  def update_status(self):
    """
      Updates the view's status bar with the current exchange rate
    """

    self.view.set_status('btc', "$%.2f (%s)" % self.get_current_exchange())

  def get_current_exchange(self):
    """
      Makes API call to exchange (determined via settings) to retrieve latest
      exchange rate.

      Exchanges:
        1 - Mt.Gox
        2 - Bitfloor

      Returns a tuple consisting of the current exchange rate of 1 bitcoin in USD
      as well as the name of the exchange.
    """

    settings = sublime.load_settings(__name__ + '.sublime-settings')
    exchange = settings.get('exchange')

    if exchange == 1:
      url = 'http://data.mtgox.com/api/1/BTCUSD/ticker'
      req = urlparse(url)
      resp = json.load(urlopen(req.geturl()))

      exchange_name = 'Mt.Gox'
      btc_in_usd = float(resp['return']['last']['value'])

    elif exchange == 2:
      url = 'https://api.bitfloor.com/ticker/1'
      req = urlparse(url)
      resp = json.load(urlopen(req.geturl()))

      exchange_name = 'Bitfloor'
      btc_in_usd = float(resp['price'])

    return (btc_in_usd, exchange_name)


  def on_load(self, view):
    self.view = view

    settings = sublime.load_settings(__name__ + '.sublime-settings')
    settings.add_on_change('exchange', self.update_status)
    settings.add_on_change('convert_strings', self.check_for_calc)

    sublime.set_timeout(self.update_status, 10)

  def on_post_save(self, view):
    self.view = view

    sublime.set_timeout(self.update_status, 10)
    self.check_for_calc()