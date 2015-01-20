VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box       = 'ubuntu/trusty64'
    config.vm.hostname  = 'ahoy-dev'

    # default flask server port
    config.vm.network :forwarded_port,  guest: 5000,  host: 5000
    # default gunicorn server port
    config.vm.network :forwarded_port,  guest: 3000,  host: 3000
    # default postgresql port
    config.vm.network :forwarded_port,  guest: 5432,  host: 5432

    # config vm settings
    config.vm.provider :virtualbox do |v|
        v.name = (0...8).map { (65 + rand(26)).chr }.join
        v.customize [ "modifyvm", :id, "--memory", 512 ]
    end

    # Configure shared folders

    # this is the defualt mapping
    #config.vm.synced_folder "./",  "/vagrant"

    # additional mappings
    #config.vm.synced_folder "./application",  "/var/www"


    # Provision the box
    # runs only on first vagrant up to re-provision run vagrant provision
    config.vm.provision :ansible do |ansible|
        ansible.playbook = "ansible/site.yml"
    end
end
