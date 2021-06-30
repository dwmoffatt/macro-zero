#!/bin/bash
function InstallDeps()
{
  echo "--- Installing Dependencies ---"

  sudo apt update
  sudo apt -y upgrade

  sudo apt install -y python3-pip libopenjp2-7-dev i2c-tools nodejs npm
  # sudo apt install -y libopenjp2-7-dev

  pip3 install --upgrade pip
  pip3 install -r ../requirements.txt
}

function InstallBuild()
{
  echo "--- Build React Front End ---"

  sudo systemctl stop macro-zero-startup.service
  sudo systemctl stop macro-zero-run.service

  cd ~/macro-zero/scr/frontend || return
  npm run build
}

function InstallServices()
{
  echo "--- Installing Macro-Zero Services ---"

  sudo systemctl stop macro-zero-startup.service
  sudo systemctl stop macro-zero-run.service

  sudo cp macro-zero-startup.service /lib/systemd/system
  sudo cp macro-zero-run.service /lib/systemd/system

  sudo systemctl daemon-reload
  sudo systemctl enable macro-zero-startup.service
  sudo systemctl start macro-zero-startup.service

  sudo systemctl enable macro-zero-run.service
  sudo systemctl start macro-zero-run.service
}

if [ $# -ne 1 ]; then
  echo "1 argument required of either [all|depsonly|build|services]"
  exit 1
fi


if [[ ("$1" != "all" && "$1" != "depsonly" && "$1" != "build" && "$1" != "services") ]]; then
  echo "1 argument required of either [all|depsonly|build|services]"
  exit 1
fi

case $1 in
"all")
InstallDeps
InstallBuild
InstallServices
;;
"depsonly")
InstallDeps ;;
"build")
InstallBuild ;;
"services")
InstallServices ;;
esac
