#!/bin/bash

rouge='\e[0;31m'
vert='\e[0;32m'
neutre='\e[0;m'


totalChecks=0
passedChecks=0

function checkSeDProcesses
{
	((totalChecks++))
	echo "$1 status : "
	subcomm="ps -edf |grep -v grep |grep $4 |wc -l"
	runprocs=`ssh $2@$3 "$subcomm"`
	echo " -running processes : $runprocs"
	if [ "${runprocs}" -gt "0" ]
	then
		echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "$1 OK" >> report.raw
	else	
		echo -e " -status ${rouge}DOWN${neutre}"
		echo "$1 NOK" >> report.raw
	fi
}

function checkFMSProxy
{
	((totalChecks++))
	echo "$1 Status : "
	subcomm="ps -edf |grep java |grep -v grep |grep com.sysfera.fmsproxy.FMSProxy |wc -l"
	runprocs=`ssh $2@$3 "${subcomm}"`
	echo " -running processes : $runprocs"
	if [ "${runprocs}" -gt "0" ]
	then
        	echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "$1 OK" >> report.raw
	else
        	echo -e " -status ${rouge}DOWN${neutre}"
		echo "$1 NOK" >> report.raw
	fi
}

function checkTMSProxy
{
	((totalChecks++))
	echo "$1 Status : "
	runprocs=`ssh $2@$3 'ps -edf |grep -v grep |grep tms |grep python |wc -l'`
	echo " -running processes : $runprocs"
	if [ "${runprocs}" -gt "0" ]
	then
        	echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "$1 OK" >> report.raw
	else
        	echo -e " -status ${rouge}DOWN${neutre}"
		echo "$1 NOK" >> report.raw
	fi
}


function connectWebBoard
{
	((totalChecks++))
	echo "Connect to $1 status : "
	if [ -f "cookie.webboard.connect" ]
	then
		echo " -removing old cookie"
		rm "cookie.webboard.connect"
	fi

	curl -3sk --data "j_username=${Wb_un}&j_password=${Wb_pw}" ${2}/j_spring_security_check --cookie-jar cookie.webboard.connect
  
	if [ -f "cookie.webboard.connect" ]
	then
		echo " -successfully connected to WebBoard"
		echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "Connect_to_$1 OK" >> report.raw
	else
		echo -e " -status ${rouge}DOWN${neutre}"
		echo " -make sure variables Wb_un and Wb_pw are set"
		echo "Connect_to_$1 NOK" >> report.raw
	fi

}

function checkAnyWebboardPage
{
	((totalChecks++))

	echo "Checking $1 status"
	if [ -f "cookie.webboard.connect" ]
	then
		echo " -cookie detected"
	else
		echo " -cookie not found : connecting"
		connectWebBoard "Webboard" $2
	fi
	
	curl -3sk --cookie cookie.webboard.connect $2/$3 > lastTest.out

	motif="$4"
	accessPage=`curl -3sk --cookie cookie.webboard.connect $2/$3 |grep "${motif}" | grep -v grep |wc -l`

	if [ "${accessPage}" -gt "0" ] 
	then
		echo " -access to the page : yes"
		echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "Check_$1 OK" >> report.raw
	else
		echo " -access to the page : no"
		echo -e " -status ${rouge}DOWN${neutre}"
		echo "Check_$1 NOK" >> report.raw
	fi
}


function checkWebBoardBasic
{
	((totalChecks++))
	echo "$1 status : "
	runprocs=`ssh $2@$3 'ps -edf |grep tomcat |grep webboard |wc -l'`
	echo " -running processes : $runprocs"
	accessLoginPage=`curl -3sk $4/login/auth?lang=en |grep '<title>Sign' | grep -v grep |wc -l`
	if [ "${accessLoginPage}" -gt "0" ] 
	then
		echo " -access to login page : yes"
	else
		echo " -access to login page : no"
	fi

	if [  "${runprocs}" -gt "0" ] && [ "${accessLoginPage}" -gt "0" ]
	then
        	echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "$1 OK" >> report.raw
	else
	        echo -e " -status ${rouge}DOWN${neutre}"
		echo "$1 NOK" >> report.raw
	fi
}

#Generate a json part for customer
function overallCheck
{
	CUSTOMERNAME=$1
	CUSTOMERFILE=part-${CUSTOMERNAME}.json
	failed=$(( ${totalChecks} - ${passedChecks} ))
	echo ""
	echo "Test performed : ${totalChecks}, passed : ${passedChecks}, failed : ${failed}"
	if [ "${failed}" -gt "0" ]
	then
        	echo -e "Overall status ${rouge}Problem detected${neutre}"
		echo "overall NOK" >> report.raw
		echo "failed ${failed}" >> report.raw
	else
        	echo -e "Overall status ${vert}OK${neutre}"
		echo "overall OK" >> report.raw
		echo "failed 0" >> report.raw
	fi

	rm $CUSTOMERFILE
	now=`date`
	echo "{\"date\":\"${now}\",\"nom\":\"${CUSTOMERNAME}\"," >> $CUSTOMERFILE 
	count=0
	for i in `cat report.raw`
	do
		modcount=$(( count % 2 ))
		if [ $count -gt 0 ]
		then
			if [ $modcount -eq 1 ]
			then
				echo ":" >> $CUSTOMERFILE
			else
				echo "," >> $CUSTOMERFILE
			fi
		fi
		((count++))
		echo "\"${i}\"" >> $CUSTOMERFILE
		
	done

	echo '}' >> $CUSTOMERFILE
}
function overall
{
	echo "{\"clients\":[" > output.json
	for i in `ls part-*`; do cat $i  >> output.json && echo "," >> output.json ;done
	echo "{}]}" >> output.json
	cat output.json | python -m json.tool > ../dataDeployments.json

}

function checkSSHTunnel
{
	((totalChecks++))
	echo "$1 status : "
	subcomm="ps -edf |grep $4 |grep ssh | grep -v grep |wc -l"
	runprocs=`ssh $2@$3 "$subcomm"`
	echo " -running processes : $runprocs"
	if [ "${runprocs}" -gt "0" ]
	then
	        echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "$1 OK" >> report.raw
	else
	        echo -e " -status ${rouge}DOWN${neutre}"
		echo "$1 NOK" >> report.raw
	fi
}

function testSubmitCLIJob
{

	((totalChecks++))
	echo "Command-line job submission status : "
	vishnu_conf=$1
	vishnu_connect=$2
	scriptDir=$3
	vishnu_submit=$4
	machine=$5
	script=$6
	existing_work_container=$7
	client_machine=$8

	when=$(date +%Y-%m-%d-%H.%M.%S)

	ssh ${client_machine} "VISHNU_CONFIG_FILE=${vishnu_conf} ${vishnu_connect} -u ${Wb_un} -w ${Wb_pw} && cd ${scriptDir} && VISHNU_CONFIG_FILE=${vishnu_conf} ${vishnu_submit} -r ${machine} -n \"CLI_TEST_$(date)\" -w ${existing_work_container} ${script} && echo \"RESULT:OK\" " > cli_${when}_out.txt 2> cli_${when}_err.txt
	
	
	jobid=$(cat cli_${when}_out.txt | grep "Job Id" | wc -l)
	resultok=$(cat cli_${when}_out.txt | grep "RESULT:OK" | wc -l)

	if [ "${jobid}" -gt "0" ] 
	then
		if [ "${resultok}" -gt "0" ] 
		then
			echo -e " -status ${vert}OK${neutre}"
			((passedChecks++))
		else
			echo -e " -status ${rouge}DOWN${neutre}"
			echo -e " -command exited with an error status."
		fi
	else
		echo -e " -status ${rouge}DOWN${neutre}"
		echo -e " -no job id provided."
	fi

}


#####################
#
# This function submits a job to the webboard, 
# but it requires the simplest possible 
# application (no parameters)
#
####################
function testSubmitWebBoardJob
{
	base_url=$1
	project_id=$2
	basic_appli_id=$3
	machineID=$4

	now=`date +%F-%H:%M:%S`

	echo "Web UI job submission status : "

	if [ -f "cookie.webboard.connect" ]
	then
		echo " -cookie detected"
	else
		echo " -cookie not found : connecting"
		connectWebBoard "Webboard" $1
	fi

	#Job submit
	curl -3sk --cookie cookie.webboard.connect -d "machine.id=${machineID}&application.id=${basic_appli_id}&subject=CurlTest-${now}&nbcpus=1" ${base_url}/work/save/${project_id} > wbjs.html.out

	echo " ...waiting during 10 seconds so that the job is submited"
	sleep 10

	motif="CurlTest-${now}"
	rm test.json

	((totalChecks++))
	curl -3sk -o test.json --cookie cookie.webboard.connect ${base_url}/work/getFilteredWorks/${project_id} --data "offset=0&max=10&ownerId=0&applicationId=0&searchText=&workStatus=all&machineId=0&order=desc&sort=id" 

	lines=`cat test.json | grep $motif  | wc -l`

	if [ "${lines}" -gt "0" ] 
	then
		rm test.json
		curl -3sk -o test.json --cookie cookie.webboard.connect ${base_url}/work/getFilteredWorks/${project_id} --data "offset=0&max=10&ownerId=0&applicationId=0&searchText=${motif}&workStatus=all&machineId=0&order=desc&sort=id" 

		jstatus=`cat test.json | python -m json.tool | grep status | awk -F':' '{print $2}' | awk -F'"' '{print $2}'`
		echo " -job status : ${jstatus}"
		
		echo " -job submitted : yes"
		echo -e " -status ${vert}OK${neutre}"
		((passedChecks++))
		echo "Job_submit OK" >> report.raw



	else
		echo " -job submitted : no"
		echo -e " -status ${rouge}DOWN${neutre}"
		echo "Job_submit NOK" >> report.raw
	fi
	
}

