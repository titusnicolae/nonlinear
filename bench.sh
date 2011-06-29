if [ $# -lt 2 ] ;then
  echo "missing output file and message"
else
  echo "Benchmark - $2" >$1
  for (( i = 0 ; i < 2 ; i++ ))
  do
    echo "test $i" >>$1
    ( time ./testpic.py ) >> bench.o 2>>bench.o 
  done
fi
