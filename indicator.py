#!/usr/bin/python

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as ai
import sys
import os

import watcher


class Indicator(object):
    def __init__(self):
        svg_icon = '.indicator_icon.svg'
        self.svg_file = os.getenv("HOME") + "/" + svg_icon
        self.createIcon()
        self.indicator = ai.Indicator.new("Exchange rates",
                                          "self.svg_file",
                                          ai.IndicatorCategory.OTHER)
        self.indicator.set_icon_theme_path(os.getenv("HOME"))
        self.indicator.set_status(ai.IndicatorStatus.ACTIVE)
        self.indicator_menu()
        GLib.timeout_add_seconds(5, self.indicator_menu)
        Gtk.main()

    def indicator_menu(self):
        # Get fresh info
        current_data = self.update_info()
        current_label = current_data['USDRUB']['rate']
        current_bid = current_data['USDRUB']['bid']
        current_ask = current_data['USDRUB']['ask']
        current_date = current_data['USDRUB']['date']
        current_time = current_data['USDRUB']['time']

        # Set new label and icon
        self.indicator.set_label("USDRUB " + current_label,
                                 ai.INDICATOR_SIGNAL_NEW_LABEL)
        self.indicator.set_icon(self.svg_file)

        # Menu structure
        menu = Gtk.Menu()
        submenu = Gtk.Menu()
        menu_pairs = Gtk.MenuItem("PAIRS")
        menu_pairs.set_submenu(submenu)
        submenu_pair_eurusd = Gtk.MenuItem("EURUSD")
        submenu_pair_eurrub = Gtk.MenuItem("EURRUB")

        menu_current_bid = Gtk.MenuItem("BID: " + current_bid)
        menu_current_ask = Gtk.MenuItem("ASK: " + current_ask)
        menu_current_date = Gtk.MenuItem("DATE: " + current_date)
        menu_current_time = Gtk.MenuItem("TIME: " + current_time)
        menu_settings = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PREFERENCES,
                                                         None)
        menu_exit = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT, None)
        menu_about = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT, None)
        separator = Gtk.SeparatorMenuItem()
        separator2 = Gtk.SeparatorMenuItem()

        # Bind actions
        menu_exit.connect("activate", self.indicator_quit)

        # Show menu items
        menu_pairs.show()
        submenu_pair_eurrub.show()
        submenu_pair_eurusd.show()
        menu_current_bid.show()
        menu_current_ask.show()
        menu_current_date.show()
        menu_current_time.show()
        menu_settings.show()
        menu_exit.show()
        menu_about.show()
        separator.show()
        separator2.show()

        # Append menu items
        submenu.append(submenu_pair_eurrub)
        submenu.append(submenu_pair_eurusd)
        menu.append(menu_current_bid)
        menu.append(menu_current_ask)
        menu.append(menu_current_date)
        menu.append(menu_current_time)
        menu.append(menu_pairs)
        menu.append(separator)
        menu.append(menu_settings)
        menu.append(separator2)
        menu.append(menu_about)
        menu.append(menu_exit)

        self.indicator.set_menu(menu)

        return True

    def createIcon(self):
        header = '<?xml version="1.0" standalone="no"?>' \
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' \
            '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 100 100">'

        text = '<g>' \
            '<text x="0" y="80" font-family="Verdana" font-size="50" fill="silver" ></text>' \
            '</g>'

        footer = '</svg>'

        with open(self.svg_file, "w") as f:
            f.write(header + text + footer)
            f.close()

    def update_info(self):
        current_data = watcher.get_query_info('USDRUB')
        return current_data

    def indicator_quit(self, attr):
        sys.exit(0)

if __name__ == "__main__":
    indicator = Indicator()
