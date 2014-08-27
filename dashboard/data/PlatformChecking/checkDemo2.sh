#!/bin/bash
source ../../../checking/libCheck.sh
URL="https://sysfera-ds.sysfera.com"
#WebBoard
connectWebBoard "WebBoard" $URL
checkAnyWebboardPage "WebBoard_project_list_page" $URL "project/list?lang=en" "<title>Project list"
overallCheck "demo2"
