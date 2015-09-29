#!/bin/sh
# Usage: ./sustc-cas-login-wget.sh [username] [password] [bind-address]

DOWN="wget -qO-"
if [ -n "$3" ]; then
DOWN="$DOWN --bind-address $3"
fi
FORM=`$DOWN baidu.com 2> /dev/null`
if echo $FORM | grep -q "/cas/login"
then
DATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "[$DATE] Logging..."
ACTION=`echo "$FORM" | grep "<form " | sed 's/.*action="\(.*\)" .*/\1/'`
LT=`echo "$FORM" | grep '<input type="hidden" name="lt" ' | sed 's/.*value="\(.*\)" .*/\1/'`
EXEC=`echo "$FORM" | grep '<input type="hidden" name="execution" ' | sed 's/.*value="\(.*\)" .*/\1/'`
DATA="username=$1&password=$2&lt=$LT&execution=$EXEC&_eventId=submit&submit=LOGIN"
RESULT=`$DOWN --post-data="$DATA" "http://weblogin.sustc.edu.cn$ACTION" 2> /dev/null`
if echo $RESULT | grep -q "<h2>success"
then
echo "Success"
else
echo "Failed"
fi
fi
exit 0
