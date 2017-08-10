# Defines our Vagrant environment
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Specify minimum Vagrant version and Vagrant API version
Vagrant.require_version '>= 1.9.1'
VAGRANTFILE_API_VERSION = '2'.freeze

# Require YAML module
require 'yaml'

# Read YAML file with box details
cfg = YAML.load_file('config.yml')
groups = cfg['groups']

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Setup Inventory File
  File.open('server/inventory.ini', 'w') do |f|
    groups.each do |group|
      group['servers'].each do |server|
        if server['type'] == 'master'
          f.write "#{server['name']}  ansible_connection=local\n"
        else
          f.write "#{server['name']}  ansible_ssh_host=#{server['ip']}\n"
        end
      end
    end

    groups.each do |group|
      f.write "[#{group['group_name']}]\n"
      group['servers'].each do |server|
        f.write "#{server['name']}\n"
      end
    end
  end

  # Setup bootstrap
  groups.each do |group|
    group['servers'].each do |server|
      File.open("temp/bootstrap-#{server['name']}.sh", 'w') do |f|
        f.write "#!/usr/bin/env bash\n"
        f.write "su vagrant <<'EOF'\n"
        f.write "cp server/keys/private ~/.ssh/id_rsa\n"
        f.write "cp server/keys/public ~/.ssh/id_rsa.pub\n"
        f.write "cp server/keys/public ~/.ssh/authorized_keys\n"
        f.write "chmod 0600 ~/.ssh/*\n"
        f.write "EOF\n"
      end
    end
  end

  # setup hostmanager
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = false
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false

  # ssh settings
  config.ssh.insert_key = false
  config.ssh.private_key_path = [
    'server/keys/private',
    '~/.vagrant.d/insecure_private_key'
  ]

  # setup nodes
  groups.each do |group|
    group['servers'].each do |server|
      config.vm.define server['name'] do |srv_config|
        srv_config.vm.box = server['box']
        srv_config.vm.hostname = server['name']

        # Forward oracle port
        srv_config.vm.network :private_network, ip: server['ip']

        server['forwarded_ports']&.each do |port|
          srv_config.vm.network :forwarded_port,
                                guest: port['guest'],
                                host: port['host']
        end

        server['synced_folders']&.each do |folder|
          srv_config.vm.synced_folder folder['guest'],
                                      folder['host'],
                                      create: true
        end

        # Provider-specific configuration so you can fine-tune various backing
        # providers for Vagrant. These expose provider-specific options.
        srv_config.vm.provider :virtualbox do |vb|
          # Use VBoxManage to customize the VM
          vb.customize ['modifyvm', :id,
                        '--name', server['name'],
                        '--memory', server['memory']]
        end

        srv_config.vm.provision :shell do |s|
          s.path = "temp/bootstrap-#{server['name']}.sh"
        end

        if server['type'] == 'master'
          srv_config.vm.provision 'ansible_local' do |ansible|
            ansible.version = 'latest'
            ansible.provisioning_path = '/home/vagrant/server/'
            ansible.playbook = 'setup.yml'
            ansible.install = true
            ansible.install_mode = :pip
            ansible.sudo = true
            ansible.verbose = false
            ansible.limit = 'all'
            ansible.inventory_path = '/home/vagrant/server/inventory.ini'
          end
        end
      end
    end
  end
end