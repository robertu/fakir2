DOMAIN=fakir.1kb.pl

APPUSER=jakub
APPGROUP=jakub
APPPORT=8811

# you can set the value of `geckodriver` to particular version number instead of latest one (for ex. 0.22.0)
geckodriver=$(shell curl https://github.com/mozilla/geckodriver/releases.atom 2>/dev/null| grep -e ">v[0-9]" |head -1|sed "s/[\/\ \<\>a-z]//g")

# you can set the value of `chromedriver` to particular version number instead of latest one
chromedriver=$(shell curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)

pythonversion=3.9.2

nodeversion=14.16.0

include Makefile.rules.mk
