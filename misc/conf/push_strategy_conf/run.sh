/usr/bin/spark-submit --driver-memory 1G --executor-memory 2G --executor-cores 2 --num-executors 2 --conf
"spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 -XX:+PrintFlagsFinal
-XX:+PrintReferenceGC -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintAdaptiveSizePolicy
-XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark -XX:+HeapDumpOnOutOfMemoryError "
--py-files /home/admin/vodpush/vodpush.zip /home/admin/vodpush/main.py