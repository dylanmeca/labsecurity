#!/bin/bash
clear
echo -e "\e[36mInstalling lab_tool....\e[0m"
git clone https://github.com/dylan14567/lab_tool
cd lab_tool
chmod +x *
python3 setup.py install
cd
rm -rf lab_tool
echo -e "\e[36mComplete installation use the lab tool command to start the framework\e[0m"
