#!/bin/bash

# qtile requirements and dependencies
sudo apt install -y git python3-pip python3-xcffib python3-cairocffi pipx
# qtile download and installation
pipx install "git+https://github.com/qtile/qtile.git"
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
sudo apt install -y picom rofi qalculate-gtk vim geany geany-plugin-treebrowser mpv lxappearance arc-theme udiskie lxpolkit ntfs-3g
