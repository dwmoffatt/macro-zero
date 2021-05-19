#!/bin/bash
function InstallDeps()
{
  echo "--- Installing Dependencies ---"

  sudo apt update
  sudo apt -y upgrade

  sudo apt install -y python3-pip
  sudo apt install -y libopenjp2-7-dev

  pip3 install --upgrade pip
  pip3 install -r ../requirements.txt
}

function InstallMain()
{
  echo "--- Installing Macro-Zero ---"
  
  sudo cp ../../macro-zero /usr/bin/
}

function InstallServices()
{
  echo "--- Installing Macro-Zero Services ---"
}

if [ $# -ne 1 ]; then
    echo "1 argument required of either [all|depsonly|main|services]"
    exit 1
fi


if [[ ("$1" != "all" && "$1" != "depsonly" && "$1" != "main" && "$1" != "services") ]]; then
  echo "1 argument required of either [all|depsonly|main|services]"
  exit 1
fi

case $1 in
"all")
InstallDeps
InstallMain
InstallServices
;;
"depsonly")
InstallDeps ;;
"main")
InstallMain ;;
"services")
InstallServices ;;
esac
