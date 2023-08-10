#!/bin/bash
sudo apt install -y git python3-pip python3-xcffib python3-cairocffi pipx

pipx install "git+https://github.com/qtile/qtile.git"
pipx ensurepath

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
