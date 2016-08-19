
sudo apt-get remove fake-hwclock
sudo rm /etc/cron.hourly/fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo rm /etc/init.d/fake-hwclock
