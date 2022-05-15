#!/bin/bash

. ./unimelb-COMP90024-2022-grp-49-openrc.sh; ansible-playbook -i ./inventory/hosts.ini deploy-frontend.yaml