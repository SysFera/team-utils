#!/bin/bash

###########################
# CONFIG

#Where is the xmssed binary we will use?
xmssed_bin=/homegpfs/idris/ebiothon/vishnu1/softs/vishnu.V4.0.0.RC22/sbin/xmssed

#Which is the config file to run the SeD?
config_file=/homegpfs/idris/ebiothon/vishnu1/runscripts/etc/vishnu.cfg

#Where do you want to store the log files.
logdir=/homegpfs/idris/ebiothon/vishnu1/runscripts/logs

#How many xms SeDs should be running? (2 in normal mode, 3 in ssl mode)
optimal_num_process=3



############################
# SCRIPT

mkdir -p ${logdir}

function killXmsSeD
{
	killall -s 9 xmssed
}

function runXmsSeD
{
	when=$(date +%Y-%m-%d-%H.%M.%S)
	${xmssed_bin} ${config_file} 1> ${logdir}/log-${when}-xmssed.out 2> ${logdir}/log-${when}-xmssed.err &
}

function countXmsSeDProcess
{
	num=$(ps -edf | grep xmssed | grep -v grep | wc -l)
	echo ${num}
}

function isXmsSeDDamaged
{
	running=$(countXmsSeDProcess)
	if [ ${running} -lt ${optimal_num_process} ] 
	then
		echo "yes"
	else
		echo "no"
	fi
}

function ressurectXmsSeD
{
	killXmsSeD
	sleep 2
	runXmsSeD
}


runXmsSeD
while [ "${stop_xmssed}x" != "truex" ]
do
	if [ $(isXmsSeDDamaged) == "yes" ]
	then
		when=$(date +%Y-%m-%d-%H.%M.%S)	
		day=$(date +%Y-%m-%d)
		echo "${when} : Test failed - relaunching seds." >> ${logdir}/keepAlive.${day}.log
		ressurectXmsSeD
	else
		when=$(date +%Y-%m-%d-%H.%M.%S)	
		day=$(date +%Y-%m-%d)
		echo "${when} : Test passed." >> ${logdir}/keepAlive.${day}.log
	fi
	sleep 30
done
killXmsSeD
