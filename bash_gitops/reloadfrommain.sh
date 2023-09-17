#!/bin/sh
set -e
git checkout main
sudo bash bash/rebuild-clean.sh -d
sleep 15
sudo bash bash/reloadfromdump.sh
git checkout Feature-2
sudo bash bash/rebuild.sh -d
