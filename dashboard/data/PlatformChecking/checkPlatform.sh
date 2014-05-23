#!/bin/bash
#################################################
# This script can be used as a template for     #
# creating new scripts for new platforms        #
#                                               #
#################################################

pushd ~/SDS/contrib/tests
source ./libCheck.sh

#define username and password.
Wb_un="admin"
Wb_pw="admin123"
Wb_URL="http://localhost:8080"
ssh_user="ec2-user"
ssh_machine="localhost"

rm report.raw 2> /dev/null
#Processes
checkSeDProcesses "XMS_SeD" ${ssh_user} ${ssh_machine} "xmssed"

#WebBoard
checkWebBoardBasic "WebBoard_login_page" ${ssh_user} ${ssh_machine} ${Wb_URL}
connectWebBoard "WebBoard" ${Wb_URL}
checkAnyWebboardPage "WebBoard_project_list_page" ${Wb_URL} "project/list?lang=en" "<title>Project list"
checkAnyWebboardPage "WebBoard_file_manager_page" ${Wb_URL} "fileBrowser/index?lang=en" "<title>File Manager - SysFera-DS"
checkAnyWebboardPage "WebBoard_FMS:getUserHome" ${Wb_URL} "fileBrowser/getUserHome?machineId=Machine1" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:listDir" ${Wb_URL} "fileBrowser/getListDir?pwd=%2Fhome%2Fec2-user%2FSDS-backup%2Fdatabase%2F&machine=Machine1&offset=0&max=20&sort=name&order=asc&noHidden=true" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:stat" ${Wb_URL} "fileBrowser/stat?file=%2Fhome%2Fec2-user%2F.sds%2F/conf&machine=Machine1" '"result":"success"'
checkAnyWebboardPage "WebBoard_Work:getDoneRatio" ${Wb_URL} "work/getDoneRatio/1?workId=22" '{"doneRatio":100}'
testSubmitWebBoardJob ${Wb_URL} "1" "1" "1"
testSubmitCLIJob "~/.sds/vishnu.cfg" "vishnu_connect" "~/SDS/contrib/tests" "vishnu_submit_job" "Machine1" "test.sh" "24" ${ssh_machine}
#Add a global summary
overallCheck

popd
