Torberry is a Raspbian based distribution for Raspberry Pi devices whose main porpuse is to serve as a Tor transparent proxy that routes all your TCP and DNS traffic through Tor network. Main advantage is that only Tor traffic is sent/received from internet, making harder to disclose your IP address.

You can learn more about Tor in their [website](https://www.torproject.org/about/overview.html.en).

### Download ###
You have to write this image to an SD card, instructions [here](http://code.google.com/p/torberry/wiki/Installation)

[torberry-0.40.img.xz](http://torberry.googlecode.com/files/torberry-0.40.img.xz)

### Where to start ###
Once image has been written, plug in raspberry and power on. Then go to http://your.raspberry.ip

- If you don't have an additional usb network adapter plugged to your raspberry then configure your computer gateway ip address with the ip of torberry.

- If you have an additional usb network adapter plugged then go to web configuration to setup physical isolation (options are very primitive but physical isolation with eth/eth or wlan/eth as uptream/downstream can be done from the web configuration). Once this is done, if you have dhcp enabled in your computer you will receive an address from the range specified in the connection.

OR capabilities (sharing you connection as a tor relay) are disabled by default.

### Bugs ###
You can check existing bugs or open new ones in [Issues page](http://code.google.com/p/torberry/issues/list)