#!/bin/sh
# Usage: ./sustc-cas-login.sh [username] [password]

URL=`curl --head baidu.com 2> /dev/null | grep "Location: http://enet.10000.gd.cn" | sed 's/Location: //'`
if echo $URL | grep -q "http"
then
DATE=`date "+%Y-%m-%d %H:%M:%S"`
URL=`echo "$URL" | sed 's/\r$//g'`
echo "[$DATE] Logging..."
FORM=`curl -L "${URL}" 2> /dev/null`
ACTION=`echo "$FORM" | grep "<form " | sed 's/.*action="\(.*\)" .*/\1/'`
LT=`echo "$FORM" | grep '<input type="hidden" name="lt" ' | sed 's/.*value="\(.*\)" .*/\1/'`
EXEC=`echo "$FORM" | grep '<input type="hidden" name="execution" ' | sed 's/.*value="\(.*\)" .*/\1/'`
DATA="username=$1&password=$2&lt=$LT&execution=$EXEC&_eventId=submit&submit=LOGIN"
RESULT=`curl -L --data "$DATA" "http://weblogin.sustc.edu.cn$ACTION" 2> /dev/null`
if echo $RESULT | grep -q "<h2>success"
then
echo "Success"
else
echo "Failed"
fi
fi
exit 0
