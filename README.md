# BitcoinTicker

![Screenshot](https://dl.dropboxusercontent.com/u/1803181/BitcoinTicker.png)

BitcoinTicker is a Sublime Text 2 plugin that displays current Bitcoin exchange rate in status and converts arbitrary BTC values to USD.

## Installing

### Package Control

This is the simplest way to get the BitcoinTicker plugin. You can install Package Control from this site: [http://wbond.net/sublime_packages/package_control](http://wbond.net/sublime_packages/package_control)

**Note:** This plugin is currently [pending](https://github.com/wbond/package_control_channel/pull/1269) to be accepted in the main Package Control repository.

### Using Git

Go to the "Packages" directory and clone this repo:

```sh
$ git clone git://github.com/pheuter/BitcoinTicker.git
```

The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

        ~/.config/sublime-text-2/Packages/

* Windows:

        %APPDATA%/Sublime Text 2/Packages/

### Without Git

[Download](https://github.com/pheuter/BitcoinTicker/archive/master.zip) the latest source from [GitHub](https://github.com/pheuter/BitcoinTicker) and copy the BitcoinTicker folder to your "Packages" directory.

## Usage

After you finish saving a file, the status bar at the bottom of the Sublime Text Editor will automatically update with the latest ticker information depending on the exchange.

You can set the exchange of your choice under:

**Package Settings / BitcoinTicker / Settings - Default**

### Conversion

You can also perform conversions from arbitrary Bitcoin values to USD. When you save a file, BitcoinTicker will search for a string containing some BTC value and insert its conversion to USD.

Supported formats that will be searched:
  * 1 BTC
  * 0.252 btc
  * .5 btc
  * 13.303 BTC

To turn on conversion, set `convert_strings` to `true` in Settings:

**Package Settings / BitcoinTicker / Settings - Default**

## Donate

If you like this plugin and want to support future updates and development, you can send Bitcoin to the following address:

**1B3PekGBDk4cD8R6NmPoahBaMSSsqTgd52**

Thanks!