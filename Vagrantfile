# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
    # Base box to build off, and download URL for when it doesn't exist on the user's system already
    config.vm.box = "p97-base-v0.4"
    config.vm.box_url = "http://downloads.point97.io/p97-base-v0.4.box"
    # config.vm.hostname = "marine-planner"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    config.vm.forward_port 8000, 8000 # django dev server
    config.vm.forward_port 8889, 8889 # mapproxy
    config.vm.forward_port 5432, 15432 # postgresql

    # config.vm.provider :virtualbox do |vb|
    #     vb.customize ["modifyvm", :id, "--memory", 256]
    # end

    # Share an additional folder to the guest VM. The first argument is
    # an identifier, the second is the path on the guest to mount the
    # folder, and the third is the path on the host to the actual folder.
    config.vm.share_folder "project", "/home/vagrant/marine-planner", "."

    # Enable provisioning with a shell script.
    config.vm.provision :shell, :path => "scripts/vagrant_provision.sh", :args => "viewpoint2"

    # If a 'Vagrantfile.local' file exists, import any configuration settings
    # defined there into here. Vagrantfile.local is ignored in version control,
    # so this can be used to add configuration specific to this computer.
    if File.exist? "Vagrantfile.local"
        instance_eval File.read("Vagrantfile.local"), "Vagrantfile.local"
    end
end
