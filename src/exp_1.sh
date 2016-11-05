# Declare time to wait between runs
waitTime=10
proc1MemSize=5120
proc2MemSize=5120

# Run the memory intensive application on partition-1
./app-1/bandwidth -c 1 -t 1000 -m $proc1MemSize -p -19&
PID=$!
echo "Process-1 Started"

# Wait for specified time
sleep $waitTime

# Migrate the process to the second partition
taskset -p 3,4 $PID &> /dev/null
echo "Process-1 Migrated"

# Run the second process
./app-2/bandwidth -c 0 -t 1000 -m $proc2MemSize -p -19&
echo "Process-2 Started"

# Wait for specified time
sleep $waitTime

# Kill the first process
kill $PID
echo "Process-1 Killed"

# Wait for specified time
sleep $waitTime

# Kill all bandwith process instances
killall bandwidth
