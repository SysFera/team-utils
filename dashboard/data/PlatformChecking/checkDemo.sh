#!/bin/bash
source ../../../checking/libCheck.sh
Wb_un="admin"
Wb_pw="admin123"
URL="https://sysfera-ds.sysfera.com"

#Processes
checkSeDProcesses "XMS_SeD" "ec2-user" "aws-demo" "xmssed"
#WebBoard
checkWebBoardBasic "WebBoard_login_page" "ec2-user" "aws-demo" ${URL}
connectWebBoard "WebBoard" ${URL}
checkAnyWebboardPage "WebBoard_project_list_page" ${URL} "project/list?lang=en" "<title>Project list"
checkAnyWebboardPage "WebBoard_file_manager_page" ${URL} "fileBrowser/index?lang=en" "<title>File Manager - SysFera-DS"
checkAnyWebboardPage "WebBoard_FMS:getUserHome" ${URL} "fileBrowser/getUserHome?machineId=babel" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:listDir" ${URL} "fileBrowser/getListDir?pwd=%2Fhome%2Fuser-cluster1%2F&machine=cluster1&offset=0&max=20&sort=name&order=asc&noHidden=true" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:stat" ${URL} "fileBrowser/stat?file=%2Fhome%2Fuser-cluster1&machine=cluster1" '"result":"success"'
checkAnyWebboardPage "WebBoard_Work:getDoneRatio" ${URL} "work/getDoneRatio/1?workId=22" '{"doneRatio":100}'
testSubmitWebBoardJob ${URL} "15" "15" "1"
testSubmitCLIJob "/home/ec2-user/sysfera-ds/etc/vishnu.server.cfg" "vishnu_connect" "/home/ec2-user/testing" "vishnu_submit_job" "cluster1" "test.sh" "647" "aws-demo"
overallCheck "demo"

http://54.246.101.26/fileBrowser/getListDir?pwd=%2Fhome%2Fuser-cluster1%2F&machine=cluster1&offset=0&max=20&sort=name&order=asc&noHidden=true
