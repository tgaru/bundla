#!/usr/bin/env bash

#-----------------------------------------------------------#
#                   Build via PyInstaller                   #
#-----------------------------------------------------------#

start_build() {
  case "$(uname -s)" in
    Darwin)
      echo -e "\x1B[92mStart building under MacOS...\x1B[0m"
      ;;

    Linux)
      echo -e "\x1B[92mStart building under Linux...\x1B[0m"
      apt install -y binutils git python3 python3-pip
      ;;

    *)
      echo -e "\x1B[91mYour OS is currently not supported :(\x1B[0m"
      exit
      ;;
  esac

  pip3 install setuptools --upgrade
  pip3 install pyinstaller
  pip3 install -r requirements.txt
  pyinstaller --onefile bundla.py
  cp -r dist/ bundla/
  cp LICENSE.md bundla/
  cp -r configs/ bundla/configs/
  tar -zcvf "bundla-$(uname -s).tar.gz" bundla
  rm -r bundla/ dist/ build/ bundla.spec

  echo -e "\x1B[92mBuilding completed. Created file:\x1B[0m bundla-$(uname -s).tar.gz"
}

start_build