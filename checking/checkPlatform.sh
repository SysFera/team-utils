#!/bin/bash
#################################################
# This script can be used as a template for     #
# creating new scripts for new platforms        #
#                                               #
#################################################
if [  -z "$SYSFERA_DS_ROOT" ];
then 
   echo "SYSFERA_DS_ROOT must be set. Exit"
   exit -1
fi
if [ ! -f ${SYSFERA_DS_ROOT}/etc/check.conf ];
then
   
   echo "${SYSFERA_DS_ROOT}/etc/check.conf must exist. Exit"
   exit -1
fi

source ${SYSFERA_DS_ROOT}/etc/check.conf

pushd ${SYSFERA_DS_ROOT}/contrib/tests

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
#Add a global summary
overallCheck

popd
