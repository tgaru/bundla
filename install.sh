#!/usr/bin/env bash

#-----------------------------------------------------------#
#                      Installing Bundla                    #
#-----------------------------------------------------------#

BUNDLA_VERSION_TAG="v1.0.0"

dependency_init() {
  git_installed="$(command -v git)"
  docker_installed="$(command -v docker)"
  compose_installed="$(command -v docker-compose)"
}

dependency_checking() {
  dependency_init
  if  [ ! -x "${git_installed}" ] ||
      [ ! -x "${docker_installed}" ] ||
      [ ! -x "${compose_installed}" ]
  then
      echo -e "\x1B[91mError! You must have software installed: Git, Docker, Docker Compose\x1B[0m"
  fi
}

installation_bundla() {
  echo -e "\x1B[92mInstall Bundla...\x1B[0m"
  curl -L "https://github.com/tgaru/bundla/releases/download/${BUNDLA_VERSION_TAG}/bundla-$(uname -s).tar.gz" -o /tmp/bundla.tar.gz
  tar -zxvf /tmp/bundla.tar.gz -C /tmp/ > /dev/null 2>&1
  mv /tmp/bundla/bundla /usr/local/bin/
  mkdir "$HOME/.bundla/"
  mv /tmp/bundla/LICENSE.md "$HOME/.bundla/"
  mv /tmp/bundla/configs/ "$HOME/.bundla/configs/"
  rm -r /tmp/bundla/ /tmp/bundla.tar.gz

  echo ''
  echo -e "\x1B[92mBundla is installed! \x1B[0mRun: \x1B[95mbundla help\x1B[0m"
  echo ''
}

user_confirmation() {
  echo -n "Continue? (y/n) [y]: "

  read -r item
  case "$item" in
      n|N)
        exit
        ;;
  esac
}

start_installation() {
  case "$(uname -s)" in
    Darwin)
      echo -e "\x1B[93mBundla will be installed on your OS.\x1B[0m"
      user_confirmation
      dependency_checking
      installation_bundla
      ;;

    Linux)
      echo -e "\x1B[93mAttention! Installing software: Bundla, Git, Docker, Docker Compose\x1B[0m"
      user_confirmation
      dependency_init

      if  [ ! -x "${git_installed}" ] ||
          [ ! -x "${docker_installed}" ] ||
          [ ! -x "${compose_installed}" ]
      then
          echo -e "\x1B[92mSystem update...\x1B[0m"
          apt update -y

          echo -e "\x1B[92mSystem upgrade...\x1B[0m"
          apt upgrade -y
      fi

      if [ ! -x "${git_installed}" ]; then
        echo -e "\x1B[92mInstall Git...\x1B[0m"
        apt install -y git
      fi

      if [ ! -x "${docker_installed}" ]; then
        echo -e "\x1B[92mInstall Docker...\x1B[0m"
        wget -qO- https://get.docker.com/ | sh
      fi

      if [ ! -x "${compose_installed}" ]; then
        echo -e "\x1B[92mInstall Docker Compose...\x1B[0m"
        curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
      fi

      dependency_checking
      installation_bundla
      ;;
    *)
      echo -e "\x1B[91mYour OS is currently not supported :(\x1B[0m"
      ;;
  esac
}

start_installation