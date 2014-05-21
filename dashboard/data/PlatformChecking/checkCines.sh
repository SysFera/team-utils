#!/bin/bash
source ./libCheck.sh
Wb_un="sysfera"
Wb_pw="GraalSystems"
URL="http://cristal2.cines.fr:8080"
connectWebBoard "WebBoard" ${URL}
checkAnyWebboardPage "WebBoard_project_list_page" ${URL} "project/list?lang=en" "<title>Project list"



