#!/usr/bin/env python3
import os
import sys
import shutil
import datetime
import time

dns_config = [
        "",
        "#===BEGINS YOUTUBE BLOCKER CONFIG===#",
        "#",
        "# Do not manually edit - control using youtubectl.py",
        "#",
        "zone \"youtubeblocker\" {type master; file \"/etc/bind/db.youtube\"; allow-query {none;}; };",
        "#===ENDING YOUTUBE BLOCKER CONFIG===#",
        ""
]

def build_config_stanza():
    return "\n".join(dns_config)

dns_prefix = [
        "$TTL 30S",
        "@                      SOA LOCALHOST. named-mgr.example.com (1 1h 15m 30d 30s)",
        "                       NS LOCALHOST.",
        "",
        "; YOUTUBE BLOCKER ZONE FILE",
        "; YOUTUBE IS CURRENTLY %BLOCKED%",
        ""
]

youtube_domains = [
    "youtube.com",
    "googlevideo.com",
    "youtube-ui.l.google.com",
    "ytimg.l.google.com",
    "ytstatic.l.google.com",
    "youtubei.googleapis.com"
]

def build_zone_file(blocked=False):
    lines = []
    for line in dns_prefix:
        lines += [ line.replace("%BLOCKED%","DISABLED" if blocked else "ENABLED") ]
    for domain in youtube_domains:
        lines += [ "%s%s CNAME ." % ("" if blocked else ";",domain) ]
    lines += [""]
    return "\n".join(lines)

if os.geteuid() != 0:
    raise Exception("You must be root to use this command")

db_path = "/etc/bind/db.youtube"
cfg_path = "/etc/bind/named.conf.local"

def slurp_config():
    with open(cfg_path,"r") as fh:
        return fh.read()

def write_config(text):
    shutil.copyfile(cfg_path,cfg_path+".BACKUP")
    with open(cfg_path,"w") as fh:
        fh.write(text)

def setup_config():
    config = slurp_config()
    stanza = build_config_stanza()
    if not stanza in config:
        config += stanza
        write_config(config)

def write_zone_file(disabled=False):
    with open(db_path,"w") as dbfh:
        dbfh.write(build_zone_file(disabled))

if not os.path.isfile(db_path):
    write_zone_file()

def bind_reload():
    os.system("systemctl --no-pager reload bind9.service")
    os.system("systemctl --no-pager status bind9.service")

def show_usage_and_exit():
    print("COMMANDS:")
    print("status\t\tshow whether youtube is enabled or disabled")
    print("enable\t\tenable youtube")
    print("disable\t\tdisable youtube")
    print("countdown N\tenable (if not already), count N minutes then disable")
    sys.exit(1)

if len(sys.argv) <= 1:
    show_usage_and_exit()

cmd_name = sys.argv[1]

def slurp_zone():
    with open(db_path,"r") as dbfh:
        return dbfh.read()

setup_config()

def is_disabled():
    return "YOUTUBE IS CURRENTLY DISABLED" in slurp_zone()

def cmd_status():
    print("YouTube is currently %s" % ("DISABLED" if is_disabled() else "ENABLED"))

def cmd_enable():
    if not is_disabled():
        print("INFO: Already enabled, nothing to do")
        return
    write_zone_file(False)
    bind_reload()
    cmd_status()

def cmd_disable():
    if is_disabled():
        print("INFO: Already disabled, nothing to do")
        return
    write_zone_file(True)
    bind_reload()
    cmd_status()

def cmd_countdown():
    if len(sys.argv) <= 2:
        print("ERROR: countdown requires minutes argument")
        sys.exit(1)
    minutes = int(sys.argv[2])
    if minutes <= 0:
        print("ERROR: bad minutes argument")
        sys.exit(1)
    if is_disabled():
        print("INFO: Enabling YouTube...")
        cmd_enable()
    else:
        print("INFO: YouTube was already enabled...")
    print("INFO: Disabling YouTube in %s minutes" % minutes)
    print("INFO: Starting at %s" % datetime.datetime.now().strftime("%H:%M:%S"))
    print("INFO: Disabled at %s" % (datetime.datetime.now() + datetime.timedelta(0,60*minutes)).strftime("%H:%M:%S"))
    time.sleep(60*minutes)
    print("INFO: Expiring at %s" % datetime.datetime.now().strftime("%H:%M:%S"))
    print("INFO: Disabling now")
    cmd_disable()
    print("")
    print("SUCCESS: Countdown completed, now exiting")

if cmd_name == "status":
    cmd_status()
elif cmd_name == "enable":
    cmd_enable()
elif cmd_name == "disable":
    cmd_disable()
elif cmd_name == "countdown":
    cmd_countdown()
else:
    print("ERROR: unrecognised command %s" % cmd_name)
    print("")
    show_usage_and_exit()
