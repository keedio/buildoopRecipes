#!/bin/bash

ask() {
    # http://djm.me/ask
    while true; do
 
        if [ "${2:-}" = "Y" ]; then
            prompt="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt="y/N"
            default=N
        else
            prompt="y/n"
            default=
        fi
 
        # Ask the question - use /dev/tty in case stdin is redirected from somewhere else
        read -p "$1 [$prompt] " REPLY </dev/tty
 
        # Default?
        if [ -z "$REPLY" ]; then
            REPLY=$default
        fi
 
        # Check if the reply is valid
        case "$REPLY" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac
 
    done
}
 

echo "Fw1-loggrabber requires the Checkpoint OPSEC SDK. Please read below the Checkpoint terms. You have to accepot them if you wan to proceed woth the installation of Fw1-loggrabber."
echo " "                                                                                                                                            
echo "                      ##################################LICENSE AGREEMENT###########################################"
echo "This Software Download Agreement (“Agreement”) is between you (either as an individual or company) and Check Point Software Technologies Ltd. ("Check Point"), for the software and documentation provided by this Agreement (“Software”).

Check Point grants to you the ability to download and access the Software and/or any modifications, corrections, and/or updates to the Software (“Software Subscription”) for which you have registered and paid the applicable fees, only if you fully comply with the terms and conditions set forth below.  Software Subscription is made available for downloading (i) solely for customers who purchase and register a Check Point Software Subscription Program in matching quantity and SKUs relative to the Check Point Product SKUs, and (ii) only for the duration of such active registered Software Subscription Program.

The Software is licensed to you under the applicable Check Point End User License Agreement (“EULA”) which accompanied your product purchase.  Any and all use of the Software and Software Subscription is governed exclusively by that EULA, the terms and conditions of which are incorporated by reference herein.  See the EULA for the specific language governing permissions and limitations under the EULA.  In the event that you do not agree with the terms of the EULA or this Agreement, then you must immediately delete all copies of the Software from your computer system and back-up system(s).  Failure to comply with the EULA limitations and this Agreement will result in termination of your right to use of the Software.

All title and copyrights in and to the Software and Software Subscription are owned by Check Point and its licensors.  Any use, reproduction, or distribution of the components of the Software and Software Subscription to anyone that has not validly registered and purchased such items, or any dissemination not in accordance with the EULA, is expressly prohibited by law and may result in severe civil and criminal penalties.  Violators will be prosecuted to the maximum extent possible.

If you are downloading a limited availability product, it may not be disseminated in any fashion.  Unless you have procured support services from Check Point under the terms of Check Point’s applicable Service Level Agreement, Check Point has no obligation to provide to you any support for this limited availability product.This Software is subject to Israel and United States export control laws. Prior to exporting please inquire as to the Software’s export classification.  Under no circumstances may Software be exported to: Cuba, Iran , North Korea, Sudan and Syria.

SOFTWARE AND SOFTWARE SUBSCRIPTION IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, INCLUDING, WITHOUT LIMITATION, THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  IN NO EVENT SHALL CHECK POINT OR ITS SUPPLIERS OR DISTRIBUTORS BE LIABLE TO YOU OR ANY OTHER PERSON FOR ANY INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES OF ANY KIND INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF PROFITS OR ANY OTHER COMMERCIAL LOSS."

if ask "Do you accept the OPSEC  license terms?"; then
    echo "Proceeding with the installation"
else
    echo "You did not accept the OPSEC license terms, stopping installation"
    exit 2
fi

echo" "
echo "Downloading the SDK" 
wget -O mainpage   http://supportcontent.checkpoint.com/file_download?id=7385
link=`egrep  http:\/\/dl3.checkpoint.com\/paid\/9a\/OPSEC_SDK_6.0_Linux\.zip.+\.zip mainpage  -o | head`
curl -H "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" -H "Accept-Encoding:gzip, deflate" -H "Accept-Language:es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3" -H "Connection:keep-alive"  -H "Host:dl3.checkpoint.com" -H "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0" "$link" -o opsec-test.zip

err=$?
if [ $err -ne 0 ]
then
    echo "Download of the SDK Failed with error code $err"
    exit $err
fi


unzip opsec-test.zip
err=$?
if [ $err -ne 0 ]
then
    echo "Unzip of the SDK failed  with error code $err"
    exit $err
fi

tar zxvf OPSEC_SDK_6_0.linux30.tar.gz 
err=$?
if [ $err -ne 0 ]
then
    echo "Untar of the SDK libraries failed  with error code $err"
    exit $err
fi

echo "Installing the SDK libraries in /usr/lig"
cp pkg_rel/lib/release.dynamic/* /usr/lib
err=$?
if [ $err -ne 0 ]
then
    echo "Installation of the SDK libraries failed  with error code $err"
    exit $err
fi

tar zxvf RoamAdmin_linux30.tar.gz
if [ $err -ne 0 ]
then
    echo "Untar of tools Roadadmin failed  with error code $err"
    exit $err
fi

tar zxvf OpsecSicUtils_linux30.tar.gz
if [ $err -ne 0 ]
then
    echo "Untar of OpsecSicUtils failed  with error code $err"
    exit $err
fi

cp linux30/* /usr/bin/.
if [ $err -ne 0 ]
then
    echo "Installation of SDK tools failed  with error code $err"
    exit $err
fi

