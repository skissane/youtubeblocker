#!/bin/bash

#
# *** YouTube Control CGI script ***
#
# For this to work, you need to do the following:
# 1) sudo apt install apache2
# 2) sudo a2enmod cgi
# 3) sudo systemctl restart apache2
# 4) sudo visudo and add following lines to sudoers:
#         www-data ALL=(ALL:ALL) NOPASSWD: /root/youtubectl.py enable
#         www-data ALL=(ALL:ALL) NOPASSWD: /root/youtubectl.py disable
#         www-data ALL=(ALL:ALL) NOPASSWD: /root/youtubectl.py status
#    That assumes you put youtubectl.py in root's home directory.
# 5) sudo cp youtubectl.cgi /usr/lib/cgi-bin
# 6) sudo chmod a+x /usr/lib/cgi-bin/youtubectl.cgi
#
# Now you can access http://IP/cgi-bin/youtubectl.cgi

echo "Content-type: text/html; charset=UTF-8"
echo ""
echo "<h1>YouTube Control</h1>"
echo "<pre>"

BODY=""
[ "${REQUEST_METHOD}" = "POST" ] && BODY="$(cat)"

if [ "${BODY}" = "ENABLE=ENABLE" ]; then
	sudo /root/youtubectl.py enable
elif [ "${BODY}" = "DISABLE=DISABLE" ]; then
	sudo /root/youtubectl.py disable
else
	sudo /root/youtubectl.py status
fi
echo "</pre>"
echo "<form action='' method='post'>"
echo "<input type=submit name=ENABLE value=ENABLE>"
echo "<input type=submit name=DISABLE value=DISABLE>"
echo "</form>"
