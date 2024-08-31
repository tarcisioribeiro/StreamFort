#!/bin/bash

sleep 1
sudo systemctl stop pmscript.service
sleep 1
sudo systemctl start pmscript.service
