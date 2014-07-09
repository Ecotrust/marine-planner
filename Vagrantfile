# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "precise32"
    config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    config.vm.network :forwarded_port, guest: 80, host: 8080  # nginx
    config.vm.network :forwarded_port, guest: 8889, host: 8889  # mapproxy
    config.vm.network :forwarded_port, guest: 8000, host: 8000  # django dev server
    config.vm.network :forwarded_port, guest: 5432, host: 15432  # postgresql

    config.vm.hostname = "marine-planner"

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 256]
    end

    config.vm.provision "ansible" do |ansible|
      ansible.sudo = true
      ansible.playbook = "../devops/provisioning/vagrant.yml"
      ansible.extra_vars = {
            repo: 'https://github.com/point97/marine-planner.git',
            branch: 'wcodp-md-staging',
            name: 'marine-planner',
            app: 'mp',
            local_settings: 'mp/settings_local.py',
            settings: 'settings',
            assets_dir: 'media',
            redis: false,
            installmedia: true,
            enable_sharing: true,
            gplus: {
                key: '40588472264-7qt1n9prnkpj40ivnuuck4jcntbknluk.apps.googleusercontent.com',
                secret: 'e8aiVDsZGUGqyNK-8tmMq3Wv'
            },
            srids: [99996]
        }
      # ansible.inventory_path = "hosts.ini"
      # ansible.limit = "vagrant-apps"
    end

    # config.vm.provision :chef_solo do |chef|
    #     chef.cookbooks_path = "scripts/cookbooks"
    #     chef.roles_path = "scripts/roles"
    #     chef.json  = {
    #         :user => "vagrant",
    #         :servername => "example.example.com",
    #         :dbname => "marine-planner",
    #         :staticfiles => "/usr/local/apps/marine-planner/mediaroot",
    #         :postgresql => {
    #             :password => {
    #                 :postgres  => "SECRET"
    #             }
    #         },
    #         :mapproxy => {
    #             :grids => [
    #                 {
    #                     :slug => "or_lambert",
    #                     :extent => "[197752.0112, 118183.8060, 2410622.1845, 1680961.2935]",
    #                     :srs => "EPSG:2992"
    #                 }
    #             ],
    #             :proxylayers => [
    #                 {
    #                     :url => "http://www.coastalatlas.net/services/wms/?",
    #                     :title => "Oregon Coastal Atlas",
    #                     :slug => "or_coastal_atlas",
    #                     :layers => [
    #                         {
    #                             :slug => "NAIP_Orthos_2011",
    #                             :title => "NAIP Orthos 2011",
    #                             :grid => "or_lambert"
    #                         },
    #                         {
    #                             :slug => "Big_Regional_Water",
    #                             :title => "Big Regional Water",
    #                             :grid => "or_lambert"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     }
    #     chef.add_role "vagrant"
    # end
end
