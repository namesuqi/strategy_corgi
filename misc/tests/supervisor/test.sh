#!/bin/bash  
  
for((i=1;i<=1000000;i++));  
do   
echo $(expr $i \* 3 + 1);
sleep 1;
done  
