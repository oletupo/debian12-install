#!/bin/bash

# Used after debian12 xfce4 basic installation
sudo apt install -y git xserver-xorg xinit

# qtile requirements
sudo apt install -y python3-pip 
sudo apt install -y python3-xcffib
sudo apt install -y python3-cairocffi

# Allow instalation of pip  packages on base python install
sudo mv /usr/lib/python3.x/EXTERNALLY-MANAGED /usr/lib/python3.x/EXTERNALLY-MANAGED.dis

# Install qtile (use pip's argument --break-system-packages)
pip3 install qtile --break-system-packages
pip3 install psutil --break-system-packages


# Installation for Appearance management
sudo apt install -y lxappearance arc-theme

# Network File Tools/System Events
sudo apt install -y mtools

# Terminal
sudo apt install -y alacritty

# Printing
sudo apt install -y cups
sudo systemctl enable cups


# Packages needed qtile after installation
sudo apt install -y picom rofi vim qalculate-gtk geany geany-plugin-treebrowser udiskie lxpolkit ntfs-3g

# Video
sudo apt install -y mpv

# Create folders in user directory (eg. Documents,Downloads,etc.)
xdg-user-dirs-update

# Installing Lightdm
sudo apt install -y lightdm 
sudo systemctl enable lightdm

# Adding qtile.desktop to Lightdm xsessions directory
cat > ./temp << "EOF"
[Desktop Entry]
Name=Qtile
Comment=Qtile Session
Type=Application
Keywords=wm;tiling
EOF
sudo cp ./temp /usr/share/xsessions/qtile.desktop;rm ./temp
u=$USER
sudo echo "Exec=/home/$u/.local/bin/qtile start" | sudo tee -a /usr/share/xsessions/qtile.desktop

# Config files
cp -Rf .config ~/

# Fonts
cp -Rf .config ~/
# Wallpapers
cp -Rf Pictures ~/

# Scripts


# Nvidia propietary drivers

#eliminar noveau?

# Add contrib and non-free to repos
sudo cp -Rf sources.list /etc/apt/sources.list

# Driver installation
sudo apt update
sudo apt install -y nvidia-driver

sudo apt autoremove

printf "\e[1;32mDone! you can now reboot.\e[0m\n"