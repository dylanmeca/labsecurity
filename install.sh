#!/bin/bash
clear
echo -e "\e[36mInstalling lab_tool....\e[0m"
chmod +x *
python3 setup.py install
cd
rm -rf lab_tool

