# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Choix de la box Ubuntu 22.04 LTS
  config.vm.box = "ubuntu/jammy64"

  # Configuration réseau (facultatif, en mode NAT par défaut)
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Provisionnement shell pour installer Python et pip, puis psutil
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
    sudo pip3 install --upgrade pip
    sudo pip3 install psutil
  SHELL

  # Dossier partagé : synchroniser dossier du projet local avec /vagrant dans la VM
  config.vm.synced_folder ".", "/vagrant"

  # Afficher la sortie dans la console à chaque lancement
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
    vb.gui = false
  end
end
