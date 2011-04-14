# Copyright 2010 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import shutil
import sys
import subprocess

try:
    from hashlib import sha1
except ImportError:
    import sha
    def sha1(str):
        return sha.new(str)

from Cheetah.Template import Template

import zc.buildout
from isotoma.recipe import gocaptain

def split(lst):
    new_lst = []
    for itm in lst.strip().split("\n"):
        new_lst.append(itm)
    return new_lst

class Squid(object):

    """ Buildout class for Varnish """

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.buildout = buildout

        self.options["location"] = os.path.join(
                buildout["buildout"]["parts-directory"], self.name)

        # Set some default options
        self.options.setdefault("cfgfile", os.path.join(self.options["location"], "squid.conf"))

        pidfile = os.path.join(self.buildout['buildout']['directory'], "var", self.name + ".pid")
        self.options.setdefault("pidfile", pidfile)

        logdir = os.path.join(self.buildout['buildout']['directory'], "var", "log", self.name)
        self.options.setdefault("logdir", logdir)

        coredumpdir = os.path.join(options["location"], "coredump")
        self.options.setdefault("coredumpdir", coredumpdir)

        cachedir = os.path.join(self.buildout['buildout']['directory'], "var", self.name)
        self.options.setdefault("cachedir", cachedir)

        self.options.setdefault("daemon", "/usr/sbin/squid")

        self.options.setdefault("template", os.path.join(os.path.dirname(__file__), "squid.conf"))
        self.options.setdefault("config", os.path.join(self.options["location"], "squid.conf"))

        self.options.setdefault("cache", "yes")
        self.options.setdefault("cache-size", "80M")

        self.options.setdefault("connect-safe-ports", "\n".join([
            "443",          # https
            "563",          # snews
            "873",          # rsync
            ]))

        self.options.setdefault("safe-ports", "\n".join([
            "80",           # http
            "21",           # ftp
            "443",          # https
            "70",           # gopher
            "210",          # wais
            "1025-65535",   # unregistered ports
            "280",          # http-mgmt
            "488",          # gss-http
            "591",          # filemaker
            "777",          # multiling http
            "631",          # cups
            "873",          # rsync
            "901",          # SWAT
            ]))

        self.options.setdefault("localnet", "\n".join([
            "127.0.0.1/32",
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
            ]))

        self.options.setdefault("refresh-patterns", "\n".join([
            "^ftp:  1440 20% 10080",
            "^gopher: 1440 0% 1440",
            "-i (/cgi-bin/|\?) 0 0% 0",
            "(Release|Package(.gz)*)$ 0 20% 2880",
            ]))
        self.options.setdefault("default-refresh", "0 20% 4320")


        self.options.setdefault("user", "nobody")
        self.options.setdefault("group", "nobody")

        self.options.setdefault("hosts-file", '')
        self.options.setdefault("allowed-domains-file", '')
        self.options.setdefault("extra-acl", '')
        self.options.setdefault("extra-http-access", '')

        # Record a SHA1 of the template we use, so we can detect changes in subsequent runs
        self.options["__hashes_template"] = sha1(open(self.options["template"]).read()).hexdigest()

    def install(self):
        location=self.options["location"]
        if not os.path.exists(location):
            os.mkdir(location)
        self.options.created(location)

        if not os.path.exists(self.options["logdir"]):
            os.makedirs(self.options["logdir"])
        if not os.path.exists(self.options["coredumpdir"]):
            os.makedirs(self.options["coredumpdir"])

        self.add_runner()
        self.create_config()
        if not os.path.exists(self.options["cachedir"]):
            self.init_cache()
        return self.options.created()

    def update(self):
        pass

    def add_runner(self):
        target = os.path.join(self.buildout["buildout"]["bin-directory"], self.name)
        f = open(target, "wt")
        gc = gocaptain.Automatic()
        gc.write(f,
                 daemon = self.options['daemon'],
                 args = "-f %s" % self.options['cfgfile'],
                 pidfile = self.options['pidfile'],
                 name = self.name,
                 description = "%s daemon" % self.options["daemon"]
                 )
        f.close()
        os.chmod(target, 0755)
        self.options.created(target)

    def create_config(self):
        template = self.options["template"]
        config = self.options["config"]

        c = Template(open(template).read(), searchList={
            "port": self.options["port"],
            "logdir": self.options["logdir"],
            "pidfile": self.options["pidfile"],
            "cachedir": self.options["cachedir"],
            "coredumpdir": self.options["coredumpdir"],
            "cache": self.options["cache"],
            "connect_safe_ports": split(self.options["connect-safe-ports"]),
            "safe_ports": split(self.options["safe-ports"]),
            "localnet": split(self.options["localnet"]),
            "refresh_patterns": split(self.options["refresh-patterns"]),
            "default_refresh": self.options["default-refresh"],
            "hosts_file": self.options["hosts-file"],
            "allowed_domains_file": self.options["allowed-domains-file"],
            "extra_acl": split(self.options["extra-acl"]),
            "extra_http_access": split(self.options["extra-http-access"]),
            })
        open(config, "w").write(str(c))
        self.options.created(self.options["config"])

    def init_cache(self):
        os.makedirs(self.options["cachedir"])
        cmd = "%s -f %s -z" % (self.options["daemon"], self.options["cfgfile"])
        ret = subprocess.call(cmd.split())
        #FIXME: Nuff said
        assert ret == 0

