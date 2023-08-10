#!/bin/bash

# prerequisites
sudo apt install -y git pipx
# qtile download and installation
pipx install "git+https://github.com/qtile/qtile.git"
# add to qtile enviorment the psutil package for widget use
pipx inject qtile psutil
pipx ensurepath
# qtile registry for lightdm
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

# Packages needed qtile after installation
sudo apt install -y picom alacritty rofi qalculate-gtk vim geany geany-plugin-treebrowser nitrogen mpv lxappearance arc-theme udiskie lxpolkit

# copy configuration files
cp -Rf .config ~/
