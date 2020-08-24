# youtubeblocker

Turn on/off access to YouTube.

I use this with our kids.

## Setup

I have an Intel NUC running Ubuntu.

I install Bind9 and DHCP server.

On my router, I turn off DHCP so the NUC does it instead.

I then use this script to turn on/off YouTube.

It needs to run as root.

It will mostly install itself the first time you run it.

But, actually there is one little extra config change you have to make manually:

In `/etc/bind/named.conf.options`:

1. inside `options{}` block, add `response-policy{}` block (if not already present)
3. inside `response-policy{}` block, add: `zone "youtubeblocker";`


## Bypass

You can bypass on adult's computers simply by switching to non-default DNS, like 8.8.8.8

Of course, this probably isn't going to work for older children (like teenagers), who may be smart enough to change DNS settings.

But our kids are too young to work that stuff out yet.
