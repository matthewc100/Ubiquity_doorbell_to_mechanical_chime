#!/usr/bin/env bash
echo "---- UFW rules (numbered) ----"
sudo ufw status numbered || true
echo
echo "---- Listening sockets (8080/22) ----"
sudo ss -tlnp | egrep ':8080|:22' || true
