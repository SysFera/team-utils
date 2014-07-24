#!/bin/bash
source ../../../checking/libCheck.sh
Wb_un="sysfera"
Wb_pw="GraalSystems"
URL="http://graal.ens-lyon.fr:8090"
connectWebBoard "WebBoard" ${URL}
checkAnyWebboardPage "WebBoard_project_auth_page" ${URL} "login/auth" "sign in"
overallCheck "caprezo"
