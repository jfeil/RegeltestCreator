echo "Waiting 10 seconds to close the application..."
sleep 10s
# get Program process
echo "Checking if it is closed..."
if ps -p "$2" > /dev/null
then
   echo "Force closing the programm..."
   kill "$2"
   sleep 5s
   # Do something knowing the pid exists, i.e. the process with $PID is running
fi
echo "Deleting the old executable..."
rm "$1"
echo "Moving the new executable..."
mv "$3" "$1"
echo "Done! Starting the closed app!"
"$1"