#!/bin/bash


source ./libCheck.sh

#define username and password.
Wb_un="admin"
Wb_pw="admin123"

rm report.raw
#Processes
checkSeDProcesses "FMS_SeD_on_VM" "vishnu" "194.57.136.140" "fmssed"
checkSeDProcesses "UMS_SeD_on_VM" "vishnu" "194.57.136.140" "umssed"
checkSeDProcesses "TMS_SeD_on_Babel" "vishnu1" "vbabel" "tmssed"
checkSSHTunnel "SSH_tunnel_on_VM" "vishnu" "194.57.136.140" "5564:localhost:5564"
checkFMSProxy "FMS_Proxy_on_VM" "vishnu" "194.57.136.140"
checkTMSProxy "TMS_Proxy_on_VM" "vishnu" "194.57.136.140"
#WebBoard
checkWebBoardBasic "WebBoard_login_page" "vishnu" "194.57.136.140" "https://www.e-biothon.fr"
connectWebBoard "WebBoard" "https://www.e-biothon.fr"
checkAnyWebboardPage "WebBoard_project_list_page" "https://www.e-biothon.fr" "project/list?lang=en" "<title>Project list"
checkAnyWebboardPage "WebBoard_file_manager_page" "https://www.e-biothon.fr" "fileBrowser/index?lang=en" "<title>File Manager - SysFera-DS"
checkAnyWebboardPage "WebBoard_FMS:getUserHome" "https://www.e-biothon.fr" "fileBrowser/getUserHome?machineId=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:listDir" "https://www.e-biothon.fr" "fileBrowser/getListDir?pwd=%2Fworkgpfs%2Fidris%2Febiothon%2Fvishnu1&machine=babel&offset=0&max=20&sort=name&order=asc&noHidden=true" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:stat" "https://www.e-biothon.fr" "fileBrowser/stat?file=%2Fworkgpfs%2Fidris%2Febiothon/vishnu1&machine=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_Work:getDoneRatio" "https://www.e-biothon.fr" "work/getDoneRatio/3?workId=95" '{"doneRatio":100}'
testSubmitWebBoardJob "https://www.e-biothon.fr" "3" "3"
#Add a global summary
overallCheck
