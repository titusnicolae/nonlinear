if [ $# -lt 2 ] ;then
  echo "missing output file and message"
else
  echo "Benchmark - $2" >$1
  for (( i = 0 ; i < 100 ; i++ ))
  do
    echo "test $i" >>$1
    ./testpic2.py >>$1 
  done
fi
