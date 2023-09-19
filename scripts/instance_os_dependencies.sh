#!/usr/bin/env bash


# Function to check if a package is installed
#is_package_installed() {
#    dpkg -l "$1" | grep -qE '^ii'
#}

# Install dependencies if they are not already installed
#if ! is_package_installed python3-pip; then
 #   sudo apt install -y python3-pip
#fi

#if ! is_package_installed nginx; then
#    sudo apt install -y nginx
#fi

#if ! is_package_installed virtualenv; then
#    sudo apt install -y virtualenv
#fi

#if ! is_package_installed postgresql; then
    sudo apt install -y postgresql
#fi

#if ! is_package_installed redis; then
#   sudo apt install -y redis
#fi
