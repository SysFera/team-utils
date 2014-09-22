#!/bin/bash

pushd /home/jenkins/team-utils/dashboard/data/PlatformChecking/
source ../../../checking/libCheck.sh

#Customer context variable
##define username and password.
Wb_un="admin"
Wb_pw="admin123"
Wb_URL="https://www.e-biothon.fr"

#Processes
checkSeDProcesses "XMS_SeD_on_VM" "vishnu" "ebiothon-vm" "xmssed"
#WebBoard
checkWebBoardBasic "WebBoard_login_page" "vishnu" "ebiothon-vm" ${Wb_URL}
connectWebBoard "WebBoard" ${Wb_URL}
checkAnyWebboardPage "WebBoard_project_list_page" ${Wb_URL} "project/list?lang=en" "<title>Project list"
checkAnyWebboardPage "WebBoard_file_manager_page" ${Wb_URL} "fileBrowser/index?lang=en" "<title>File Manager - SysFera-DS"
checkAnyWebboardPage "WebBoard_FMS:getUserHome" ${Wb_URL} "fileBrowser/getUserHome?machineId=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:listDir" ${Wb_URL} "fileBrowser/getListDir?pwd=%2Fworkgpfs%2Fidris%2Febiothon%2Fvishnu1&machine=babel&offset=0&max=20&sort=name&order=asc&noHidden=true" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:stat" ${Wb_URL} "fileBrowser/stat?file=%2Fworkgpfs%2Fidris%2Febiothon/vishnu1&machine=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_Work:getDoneRatio" ${Wb_URL} "work/getDoneRatio/3?workId=95" '{"doneRatio":100}'
#testSubmitWebBoardJob ${Wb_URL} "3" "3" "babel"
testSubmitCLIJob "/home/vishnu/sysfera-ds/etc/vishnu.server.cfg" "vishnu_connect" "/home/vishnu/applis/scripts" "vishnu_submit_job" "babel" "test.sh" "200" "ebiothon-vm"
#Add a global summary
overallCheck "ebiothon"

popd

