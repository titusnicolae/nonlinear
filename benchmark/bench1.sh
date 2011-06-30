if [ $# -lt 2 ] ;then
  echo "missing output file and message"
else
  echo "Benchmark - $2" >$1
  for (( i = 0 ; i < 30 ; i++ ))
  do
    echo "test $i" >>$1
    ./testpic.py >>$1 
  done
fi
