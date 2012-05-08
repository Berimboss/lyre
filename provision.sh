## update apt-get
apt-get update
## Need easy_install, pip
apt-get install -y python-setuptools
## Need this for a reason unknown to me
apt-get install -y libpq-dev python-dev
## git pip to git goods!
easy_install pip
# memecache
apt-get install -y python-memcache
apt-get install -y memcache
# libevent
apt-get install -y libevent-dev
## ruby support
apt-get install -y ruby-full
## get git for pip via git
apt-get install git-core
## Ruby gems
wget http://production.cf.rubygems.org/rubygems/rubygems-1.8.17.tgz
tar -zxvf rubygems-1.8.17.tgz
ruby rubygems-1.8.17/setup.rb
rm rubygems-1.8.17.tgz
rm -rf rubygems-1.8.17/
## Screw old rubygems
mv /usr/bin/gem1.8 /usr/bin/gem
## foreman
gem install foreman --no-ri --no-rdoc
