#!/bin/bash

keys_path=~/sysfera-ds/etc/httpcert
cd ${keys_path}

private_key="www.e-biothon.fr.key"
certificate="cert-23358-www.e-biothon.fr.pem"
ordered_authority_certificate_chain="chain-23358-www.e-biothon.fr-1-TERENA_SSL_CA.pem chain-23358-www.e-biothon.fr-2-UTN-USERFirst-Hardware.pem chain-23358-www.e-biothon.fr-3-AddTrust_External_CA_Root.pem"


echo "Private key : ${private_key}"
echo "Certificate : ${certificate}"

echo "md5 check of the private key : "
pkmd5=`openssl rsa -noout -modulus -in ${private_key} | openssl md5`
echo "${pkmd5}"
echo "md5 check of the signed certificate : "
scmd5=`openssl x509 -noout -modulus -in ${certificate} | openssl md5`
echo "${scmd5}"

if [ "${scmd5}" != "${pkmd5}" ]
then
	echo "Signed certificate does not correspond to private key."
	echo "Aborting."
	exit 1	
else
	echo "Key corresponding : OK"
fi

echo "Generating concatenated CA file"
if [ -f "CA.crt" ]
then
	echo "CA.crt file already exists."
	echo "Aborting."
	exit 2
else
	for it in ${ordered_authority_certificate_chain}
	do
		cat ${it} >> CA.crt
	done
	echo "CA.crt file created."
fi

echo "Checking that certificate corresponds to CA certification chain : "
cacertok=`openssl verify -CAfile CA.crt ${certificate}`

check=`echo "${cacertok}" | grep "${certificate}" | grep "OK" | grep -v grep | wc -l`

echo "${cacertok}"
echo "${check}"

if [ "${check}" == "1" ]
then
	echo "Check : OK"
else
	echo "The certificate does not appears to be signed by the CA chain."
	echo "Aborting"
	exit 3
fi

echo "Converting Keys : "
echo "Step 1 : adding a passphrase to your private key"

openssl rsa -in ${private_key} -des3 -out protected-${private_key}

echo "Step 2 : Generating a pkcs12 Keystore"
echo "hint : remember the export password you will define as it will be asked in the next step"
openssl pkcs12 -export -in ${certificate} -inkey protected-${private_key} -out ${private_key}_keystore.p12 -name tomcat -CAfile CA.crt -caname root -chain


echo "Step 3 : Generating the jqs keystore"
echo "hint 1 : The destination passphrase must be the same as the passphrase that we added to protect the private key."
echo "hint 2 : The source passphrase must be the export password you entered in the previous step"

keytool -importkeystore -srckeystore ${private_key}_keystore.p12 -srcstoretype pkcs12 -srcalias tomcat -destkeystore ${private_key}_keystore.jks -deststoretype jks  -destalias tomcat


