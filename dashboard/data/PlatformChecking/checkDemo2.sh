#!/bin/bash
source ../../../checking/libCheck.sh
URL="http://54.246.101.26:8080"
#WebBoard
connectWebBoard "WebBoard" $URL
checkAnyWebboardPage "WebBoard_project_list_page" $URL "project/list?lang=en" "<title>Project list"
overallCheck "demo2"