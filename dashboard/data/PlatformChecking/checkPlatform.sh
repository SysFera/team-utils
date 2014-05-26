#!/bin/bash
#################################################
# This script can be used as a template for     #
# creating new scripts for new platforms        #
#                                               #
#################################################


installation_path=~

#define username and password.
Wb_un="admin"
Wb_pw="admin123"
Wb_URL="http://localhost:8080"
ssh_user="ec2-user"
ssh_machine="localhost"
machineName="Machine1"
machineId=1

listdir_testpath="%2Fhome%2Fec2-user%2FSDS-backup%2Fdatabase%2F"
simple_application_projectId=1
simple_applicationId=1
sample_completedJobId=22
sample_containerJob=24

pushd ${installation_path}/SDS/contrib/tests
source ./libCheck.sh

rm report.raw 2> /dev/null
#Processes
checkSeDProcesses "XMS_SeD" ${ssh_user} ${ssh_machine} "xmssed"

#WebBoard
checkWebBoardBasic "WebBoard_login_page" ${ssh_user} ${ssh_machine} ${Wb_URL}
connectWebBoard "WebBoard" ${Wb_URL}
checkAnyWebboardPage "WebBoard_project_list_page" ${Wb_URL} "project/list?lang=en" "<title>Project list"
checkAnyWebboardPage "WebBoard_file_manager_page" ${Wb_URL} "fileBrowser/index?lang=en" "<title>File Manager - SysFera-DS"
checkAnyWebboardPage "WebBoard_FMS:getUserHome" ${Wb_URL} "fileBrowser/getUserHome?machineId=${machineName}" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:listDir" ${Wb_URL} "fileBrowser/getListDir?pwd=${listdir_testpath}&machine=${machineName}&offset=0&max=20&sort=name&order=asc&noHidden=true" '"result":"success"'
checkAnyWebboardPage "WebBoard_FMS:stat" ${Wb_URL} "fileBrowser/stat?file=${listdir_testpath}&machine=${machineName}" '"result":"success"'
checkAnyWebboardPage "WebBoard_Work:getDoneRatio" ${Wb_URL} "work/getDoneRatio/${simple_application_projectId}?workId=${sample_completedJobId}" '{"doneRatio":100}'
testSubmitWebBoardJob ${Wb_URL} "${simple_application_projectId}" "${simple_application_projectId}" "${machineId}"
testSubmitCLIJob "~/.sds/vishnu.cfg" "vishnu_connect" "${installation_path}/SDS/contrib/tests" "vishnu_submit_job" ${machineName} "test.sh" "${sample_containerJob}" ${ssh_machine}
#Add a global summary
overallCheck

popd
