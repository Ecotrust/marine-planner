# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "precise32"
    config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    config.vm.network :forwarded_port, guest: 80, host: 8010  # nginx
    config.vm.network :forwarded_port, guest: 8000, host: 8000  # django dev server
    config.vm.network :forwarded_port, guest: 5432, host: 15432  # postgresql

    config.vm.hostname = "marine-planner"

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 256]
    end

    config.vm.provision :chef_solo do |chef|
        chef.cookbooks_path = "scripts/cookbooks"
        chef.roles_path = "scripts/roles"
        chef.json  = {
            :user => "vagrant",
            :servername => "example.example.com",
            :dbname => "marine-planner",
            :staticfiles => "/usr/local/apps/marine-planner/mediaroot",
            :postgresql => {
                :password => {
                    :postgres  => "SECRET"
                }
            }
        }
        chef.add_role "vagrant"
    end
end
