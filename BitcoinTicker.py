import sublime
import sublime_plugin
import urllib2
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

      if len(regions) > 0:
        region = regions[0]
        amount = float(extractions[0])
        exchange_name, btc_in_usd = self.get_current_exchange()
        result = btc_in_usd * amount

        edit = self.view.begin_edit()
        self.view.replace(edit, region, "(%s) $%.2f" % (exchange_name, result))
        self.view.end_edit(edit)

        self.view.sel().clear()
        self.view.sel().add(self.view.line(region))
        self.view.show_at_center(region)

  def update_status(self):
    """
      Updates the view's status bar with the current exchange rate
    """

    self.view.set_status('btc', "(%s) $%.2f" % self.get_current_exchange())

  def get_current_exchange(self):
    """
      Makes API call to exchange (determined via settings) to retrieve latest
      exchange rate.

      Exchanges:
        1 - Mt.Gox
        2 - Bitfloor

      Returns a tuple consisting of the exchange name and the current rate of
      1 bitcoin in USD
    """

    settings = sublime.load_settings(__name__ + '.sublime-settings')
    exchange = settings.get('exchange')

    if exchange == 1:
      url = 'http://data.mtgox.com/api/1/BTCUSD/ticker'
      req = urllib2.Request(url)
      resp = json.load(urllib2.urlopen(req))

      exchange_name = 'Mt.Gox'
      btc_in_usd = float(resp['return']['last']['value'])

    elif exchange == 2:
      url = 'https://api.bitfloor.com/ticker/1'
      req = urllib2.Request(url)
      resp = json.load(urllib2.urlopen(req))

      exchange_name = 'Bitfloor'
      btc_in_usd = float(resp['price'])

    return (exchange_name, btc_in_usd)


  def on_load(self, view):
    settings = sublime.load_settings(__name__ + '.sublime-settings')
    settings.add_on_change('exchange', self.update_status)
    settings.add_on_change('convert_strings', self.check_for_calc)

  def on_post_save(self, view):
    self.view = view

    sublime.set_timeout(self.update_status, 10)
    self.check_for_calc()