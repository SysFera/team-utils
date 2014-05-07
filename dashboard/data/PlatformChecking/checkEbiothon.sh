#!/bin/bash

pushd /home/jenkins/team-utils/dashboard/data/PlatformChecking/
source ./libCheck.sh

#Customer context variable
##define username and password.
Wb_un="admin"
Wb_pw="admin123"

rm report.raw 2> /dev/null
#Processes
checkSeDProcesses "FMS_SeD_on_VM" "vishnu" "ebiothon-vm" "fmssed"
checkSeDProcesses "UMS_SeD_on_VM" "vishnu" "ebiothon-vm" "umssed"
checkSeDProcesses "TMS_SeD_on_Babel" "vishnu1" "ebiothon-babel" "tmssed"
#The ssh tunnel is not required anymore
#checkSSHTunnel "SSH_tunnel_on_VM" "vishnu" "ebiothon-vm" "5564:localhost:5564"
checkFMSProxy "FMS_Proxy_on_VM" "vishnu" "ebiothon-vm"
checkTMSProxy "TMS_Proxy_on_VM" "vishnu" "ebiothon-vm"
#WebBoard
checkWebBoardBasic "WebBoard_login_page" "vishnu" "ebiothon-vm" "https://www.e-biothon.fr"
connectWebBoard "WebBoard" "https://www.e-biothon.fr"
checkAnyWebboardPage "WebBoard_project_list_page" "https://www.e-biothon.fr" "project/list?lang=en" "<title>Project list"
checkAnyWebboardPage "WebBoard_file_manager_page" "https://www.e-biothon.fr" "fileBrowser/index?lang=en" "<title>File Manager - SysFera-DS"
checkAnyWebboardPage "WebBoard_FMS:getUserHome" "https://www.e-biothon.fr" "fileBrowser/getUserHome?machineId=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:listDir" "https://www.e-biothon.fr" "fileBrowser/getListDir?pwd=%2Fworkgpfs%2Fidris%2Febiothon%2Fvishnu1&machine=babel&offset=0&max=20&sort=name&order=asc&noHidden=true" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:stat" "https://www.e-biothon.fr" "fileBrowser/stat?file=%2Fworkgpfs%2Fidris%2Febiothon/vishnu1&machine=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_Work:getDoneRatio" "https://www.e-biothon.fr" "work/getDoneRatio/3?workId=95" '{"doneRatio":100}'
testSubmitWebBoardJob "https://www.e-biothon.fr" "3" "3"
testSubmitCLIJob "/home/vishnu/applis/etc/vishnu.cfg" "/home/vishnu/applis/vishnu/bin/vishnu_connect" "/home/vishnu/applis/scripts" "/home/vishnu/applis/vishnu/bin/vishnu_submit_job" "babel" "test.sh" "200" "ebiothon-vm"
#Add a global summary
overallCheck "ebiothon"

popd

