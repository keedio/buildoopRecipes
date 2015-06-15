#!/bin/bash

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# chkconfig: 2345 80 20
# description: Summary: Kafka is a high-throughput distributed messaging system designed for persistent messages as the common case. Throughput rather than features are the primary design constraint.  State about what has been consumed is maintained as part of the consumer not the server. Kafka is explicitly distributed. It is assumed that producers, brokers, and consumers are all spread over multiple machines.
# processname: java
# pidfile: /var/run/kafka/kafka-server.pid
### BEGIN INIT INFO
# Provides:          kafka-server
# Required-Start:    $network $local_fs
# Required-Stop:
# Should-Start:      $named
# Should-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Kafka is a high-throughput distributed messaging system designed for persistent messages as the common case.
### END INIT INFO

. /lib/lsb/init-functions

# Autodetect JAVA_HOME if not defined
if [ -f /etc/profile.d/java.sh ]; then
        . /etc/profile.d/java.sh
        [ -z "\$JAVA_HOME" ] && echo "JAVA_HOME is not defined" && exit 1
else
        echo "enviroment not properly set up"
        exit 1
fi
if [ -f /etc/profile.d/kafka.sh ]; then
	. /etc/profile.d/kafka.sh
fi

STATUS_RUNNING=0
STATUS_DEAD=1
STATUS_DEAD_AND_LOCK=2
STATUS_NOT_RUNNING=3

NAME=kafka-server
DESC="Kafka daemon"

KAFKA_HOME=${KAFKA_HOME-"/usr/lib/kafka"}
KAFKA_CONF=${KAFKA_CONF-"/etc/kafka/conf"}
KAFKA_RUN_DIR=${KAFKA_RUN-"/var/run/kafka"}
KAFKA_SHUTDOWN_TIMEOUT=${KAFKA_SHUTDOWN_TIMEOUT-10}
KAFKA_START_TIMEOUT=${KAFKA_START_TIMEOUT-10}
KAFKA_USER=${KAFKA_USER-"kafka"}

PID_FILE="$KAFKA_RUN_DIR/kafka-server.pid"

[ -d $KAFKA_RUN_DIR ] || install -d -m 0755 -o $KAFKA_USER -g $KAFKA_USER $KAFKA_RUN_DIR

start() {
    checkstatus
    status=$?
    if [ "$status" -eq "$STATUS_NOT_RUNNING" ]; then
    	printf "Starting kafka server..."
	su -s /bin/sh $KAFKA_USER -c "$KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_CONF/server.properties"
        for i in `seq $KAFKA_START_TIMEOUT`; do
	    ps ax | grep -i 'kafka\.Kafka' | grep java | grep -v grep | awk '{print $1}' > $PID_FILE
	    checkstatus
    	    if [ $? -eq $STATUS_RUNNING ]; then
        	log_success_msg ""
	    	return 0
 	    fi
	    sleep 1
	done
   fi
   
   if [ "$status" -eq "$STATUS_RUNNING" ]; then
       log_warning_msg "Kafka server is already running"
   elif [ "$status" -eq "$STATUS_DEAD" ]; then
       log_failure_msg "Kafka server is dead and pid file exists"
   elif [ "$status" -eq "$STATUS_DEAD_AND_LOCK" ]; then 
       log_failure_msg "Kafka server is dead and lock file exists"
   else
       log_failure_msg "Kafka server status is unknown"
   fi
   
   return 1
}

stop() {
    checkstatus
    status=$? 
  
  if [ "$status" -eq "$STATUS_RUNNING" ]; then
    pid=`cat $PID_FILE`
    printf "Stopping Kafka server with pid $pid..."
      if [ -n $pid ]; then
        kill -TERM $pid &>/dev/null
        for i in `seq 1 ${KAFKA_SHUTDOWN_TIMEOUT}` ; do
          kill -0 $pid  &>/dev/null || break
          sleep 1
        done
        kill -KILL $pid &>/dev/null
      fi
    kill -0 $pid  &>/dev/null && return 1
    rm -f $PID_FILE
    log_success_msg ""
    return 0
  fi

  if [ "$status" -eq "$STATUS_NOT_RUNNING" ]; then
    log_failure_msg "Kafka server is not running"
  elif [ "$status" -eq "$STATUS_DEAD" ]; then
    log_warning_msg "Kafka server is dead and pid file exists. Triying to remove it..."
    rm -f $PID_FILE
    log_success_msg "Removed"
  elif [ "$status" -eq "$STATUS_DEAD_AND_LOCK" ]; then 
    log_warning_msg "Kafka server is dead and lock file exists."
  else
    log_failure_msg "Kafka server status is unknown"
  fi

  return 1
}

restart() {
  stop
  start
}

status(){
  checkstatus
  status=$?

  if [ "$status" -eq "$STATUS_RUNNING" ];then
    log_success_msg "Kafka server is running"
    return 0
  elif [ "$status" -eq "$STATUS_NOT_RUNNING" ]; then
    log_failure_msg "Kafka server is not running"
    return 3
  elif [ "$status" -eq "$STATUS_DEAD" ]; then
    log_failure_msg "Kafka server is dead and pid file exists"
    return 1
  elif [ "$status" -eq "$STATUS_DEAD_AND_LOCK" ]; then
    log_failure_msg "Kafka server is dead and lock file exists."
    return 1
  else
    log_failure_msg "Kafka server status is unknown"
    return 1
  fi
}

checkstatus(){
  pidofproc -p $PID_FILE java > /dev/null
  return $?
}

case "$1" in
    start)
	start
	exit $?
	;;
    stop)
	stop 
	exit $?
	;;
    restart)
        restart
	exit $?
	;;
    status)
	status
	exit $?
	;;
    *)
	N=/etc/init.d/$NAME
	echo "Usage: $N {start|stop|restart|status}" >&2
	exit 1
	;;
esac
