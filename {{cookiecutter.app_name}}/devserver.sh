#!/usr/bin/env bash
# This will start api-hour with a single worker and a super-long timeout to make things easier to debug
clear && api_hour -w 1 -t 999999 -ac {{cookiecutter.app_name}}:Container
