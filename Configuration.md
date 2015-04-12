# Introduction #

Since torberry 0.30, /etc/torberry.conf is included. This file is POSIX compatible. All adjust should be made to this file.

# Parameters #

**NTPD**
NTP server hostname or IP used when booting to sync with tor

**OPERATION\_MODE**
Setup how torberry will manage the network.
Valid options are **nonphys** and **physical-isolation**

  * nonphys: eth0 will be used for upstream and downstream. Upstream will be dhcp. Clients should change their gateway IP to torberry's IP. If you set mode to nonphys then all UPSTREAM and DOWNSTREAM parameter won't be used.

  * physical-isolation: allows to choose interfaces. Also brings up a dhcpd server on downstream side.

**UPSTREAM\_IF**
Interface which will be used to connect to tor. Commonly known in routers as upstream interface.
If you choose physical-isolation this parameter is necessary

**UPSTREAM\_IP\_MODE**
Network configuration mode, you can choose **dhcp** or **manual**
If you choose physical-isolation this parameter is necessary

**UPSTREAM\_IP\_IPADDR**
IP address of the upstream interface. If you choose manual, this parameter is necessary

**UPSTREAM\_IP\_NETMASK**
Network mask of the upstream interface. If you choose manual, this parameter is necessary

**UPSTREAM\_IP\_NETWORK**
Network address of the upstream interface. If you choose manual, this parameter is necessary

**UPSTREAM\_IP\_BROADCAST**
Broadcast address of the upstream interface. If you choose manual, this parameter is necessary

**UPSTREAM\_IP\_GATEWAY**
Gateway address of the upstream interface. If you choose manual, this parameter is necessary

**UPSTREAM\_IP\_DNS**
DNS address of the upstream interface. If you choose manual, this parameter is necessary

**UPSTREAM\_WIRELESS**
If your UPSTREAM\_IF is a wireless interface then it should be set to true. Otherwise false.

**UPSTREAM\_WL\_SSID**
Wireless network name (SSID)
Necessary if upstream\_wireless is true

**UPSTREAM\_WL\_PROTO**
Wireless protocol. Currently only WPA has been tested. Probably accepts other values. Note that torberry uses wpa\_supplicant.
Necessary if upstream\_wireless is true

**UPSTREAM\_WL\_KEYMGMT**
Wireless encryption type. Currently only WPA-PSK has been tested.
Necessary if upstream\_wireless is true

**UPSTREAM\_WL\_PASSWD**
Wireless password.
Necessary if upstream\_wireless is true

**DOWNSTREAM\_IF**
This interface will server Tor to other computers. DHCP server will be enabled in this interface.
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_IP\_IPADDR**
IP address of the downstream interface
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_IP\_NETMASK**
Netmask of the downstream interface
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_IP\_NETWORK**
Network address of the downstream interface
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_IP\_BROADCAST**
Broadcast of the downstream interface
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_DHCP\_FROM**
Network address of the first IP that can be assigned by dhcpd
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_DHCP\_TO**
Network address of the last IP that can be assigned by dhcpd
If you choose physical-isolation this parameter is necessary

**DOWNSTREAM\_WIRELESS**
This will activate hostap and torberry will be a wifi router
Experimental feature that is not available yet.
Accepts true or false