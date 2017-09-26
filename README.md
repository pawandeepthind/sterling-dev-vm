# What

Project to setup multi-vm development environment for IBM Sterling 94 or 95 development with pre-required software installed on the machines. This setup uses,
  * vagrant
  * virtual box as the provider
  * Ansible to orchestrate installation of software
  
  Topology for multiple virtual machine consist of:

  * One management server where ansible is installed when machine is provisioned. (Note: This machine is the last machine, and only one in the group in config.yml and is of type master)
  * Other machines in the topology is defined using configuration 

User can bring up the machine with one command ``` vagrant up ```.

This brings up multi-vm development environments with 
  * Connected machines.
  * Public/Private keys setup for password less access
  * Ansible installed on master machine, that will trigger setup.yml
  * setup.yml can be used to setup what roles to apply on which machine or group of machine.

# How

## 1. Install Pre-requisite:

It is good to read about Vagrant and Ansible.

## Here are some of the pre-requisite (Note: It is tested on Mac OS X for now)

  * vagrant (tested with vagrant 1.9.7)
  * Virtual Box (tested with VirtualBox 5.1.26r117224)
  * Software is installed in the machines using [ansible](https://www.ansible.com/) that is installed on mgmt_server
  * Install plugins (vbguest and hostmanager)
    
  ```
  $ vagrant plugin install vagrant-vbguest
  $ vagrant plugin install vagrant-hostmanager
  ```

# Select what to install Sterling 94 or Sterling 95.
  1. Change server/group_vars/all.yml
      ```
      sterling_version: 95 # supports 94 or 95
      database_machine_name: database # this is the name of the database machine from config file
      ```
  2. Update server/setup.yml and change sterling at the roles to select on sterlingdev
  3. Copy the correct installer in server/roles/files
    1. Extract Sterling (94 or 95) installer.
    2. Rename extracted component to OM, STORE and CC

## 2. config.yml configurations

```yml
---
groups: # root for multi-vm configuration
  - group_name: database_group # group name where we can define one or more servers
    servers: #array of servers that needs to be configured in this group
      - name: database # name of the server
        type: slave # type of the server (slave or masster), note: there needs to be one machine of type master 
                    # and others should be slave. And master machine should be in the end and that gorup should have only one machine
        box: centos/7 # which vagrant box to use to setup base machine
        memory: 512 # memory that should be given to the machine
        ip: 10.0.20.20 # ip address that should be given to the machine
        synced_folders: # list of folders to setup the sync
          - { guest: "./server", host: "/home/vagrant/server" }
        forwarded_ports: # list of ports to be forwarded from the guest to host
          - { guest: 1521, host: 1521 } # oracle default port
  - group_name: appserver_group
    servers:
      - name: sterlingdev # server that will have weblogic, sterling 94 or 95, activemq installed
        type: slave
        box: centos/7
        memory: 4096
        ip: 10.0.20.30
        synced_folders: 
          - { guest: "./server", host: "/home/vagrant/server" }
        forwarded_ports:
          - { guest: 8080, host: 8080 }
          - { guest: 8787, host: 8787 } 
          - { guest: 8443, host: 8443 }
          - { guest: 7001, host: 7001 } # weblogic port
          - { guest: 8453, host: 8453 }
          - { guest: 61616, host: 8616 } # activemq port
          - { guest: 8161, host: 8161 } # activemq port
  - group_name: management_server 
    servers:
      - name: mgmt
        type: master
        box: centos/7
        memory: 256
        ip: 10.0.20.10
        synced_folders: 
          - { guest: "./server", host: "/home/vagrant/server" }
        forwarded_ports:


```

# Note: 

1. Required roles are setup, you will need to put installer files in server/roles/files folder for these roles to pickup, in case you have your own roles avialble to install the software, put them in server/roles and use setup.yml to provision the software.
2. **Links, Credentials and Ports** (Note: ip can be different depending on the ip used in config.yml)
  * Active MQ: http://10.0.20.30:8161/ admin/admin
  * Oracle DB: 
    * system@//10.0.20.20:1521/xe system/manager
    * sterling94@//10.0.20.20:1521/xe sterling94/sterling94
  * Weblogic Console: http://10.0.20.30:7001/console weblogic/weblogic123
  * Sterling 
    * Console: http://10.0.20.30:7001/smcfs/console/login.jsp admin/password
    * SBC: http://10.0.20.30:7001/sbc/sbc/login.do admin/password
    * Sterling: http://10.0.20.30:7001/isccsdev/isccs/login.do admin/password
    * Sterling Store: http://10.0.20.30:7001/wscdev/store/login.do admin/password ## user/password
    * API Tester: http://10.0.20.30:7001/smcfs/yfshttpapi/yantrahttpapitester.jsp