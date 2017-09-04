#!/bin/bash

#dataFileName=100inst_random_50proc_Cb100_Edge_tool_n03265032.csv
dataFileName=adobe-data-17_04_05-hkpp.csv
dimensionFileName=testowe.list
mainDiroctoryEndedWithSlash=/home/lolech/Hk++/1/
outputSubFolder=adobe-data-17_04_05_k2_n10-100_r10-100_e10_l5_DM/

outputMasterFolder=$mainDiroctoryEndedWithSlash$outputSubFolder #folder w ktorym stworzyc podfolder z wynikami oraz logfile
inputDataFullPath=$mainDiroctoryEndedWithSlash$dataFileName
inputDimensionNamesFullPath=$mainDiroctoryEndedWithSlash$dimensionFileName
method=-lgmm #-km
verboseMode=-v # aby wylaczyc zostaw puste
#number of repeats for each parameter setup
numberOfIterations=10
#K - number of clusters
firstKValue=2
lastKValue=2
kValueStep=1
#S - dendrogram max size
firstSValue=2147483600
lastSValue=2147483600
sValueStep=1
#N - number of alg iterations
firstNValue=10
lastNValue=100
nValueStep=10
#R - number of alg repeats
firstRValue=10
lastRValue=100
rValueStep=10
#E - epsilon used in comparision with 0 (covariuance matrix det), in program thsi parameters is used as 10^-E
firstEValue=10
lastEValue=10
eValueStep=1
#L - little value used to make covariance matrix non singular, this value is added on diagonal of each covariance matrix until its determinant is greater than 0. This value is used as 10^-L
firstLValue=5
lastLValue=5
lValueStep=1
#W - maximum number of nodes
firstWValue=500
lastWValue=500
wValueStep=1
#Fc - static center covariance matrix scalling factor
firstCfValue=$(echo "scale=2; 1.0" | bc)
lastCfValue=$(echo "scale=2; 1.0" | bc)
cfValueStep=$(echo "scale=2; 0.05" | bc)

#Fr - static center responsibility scalling factor
firstRfValue=$(echo "scale=2; 1.0" | bc)
lastRfValue=$(echo "scale=2; 1.0" | bc)
rfValueStep=$(echo "scale=2; 0.05" | bc)

cd $mainDiroctoryEndedWithSlash
mkdir $outputMasterFolder

numberOfKRunsInFloat=$(echo "scale=2; ($lastKValue - $firstKValue) / $kValueStep + 1" | bc)
numberOfSRunsInFloat=$(echo "scale=2; ($lastSValue - $firstSValue) / $sValueStep + 1" | bc)
numberOfNRunsInFloat=$(echo "scale=2; ($lastNValue - $firstNValue) / $nValueStep + 1" | bc)
numberOfRRunsInFloat=$(echo "scale=2; ($lastRValue - $firstRValue) / $rValueStep + 1" | bc)
numberOfERunsInFloat=$(echo "scale=2; ($lastEValue - $firstEValue) / $eValueStep + 1" | bc)
numberOfLRunsInFloat=$(echo "scale=2; ($lastLValue - $firstLValue) / $lValueStep + 1" | bc)
numberOfWRunsInFloat=$(echo "scale=2; ($lastWValue - $firstWValue) / $wValueStep + 1" | bc)
numberOfCfRunsInFloat=$(echo "scale=2; ($lastCfValue - $firstCfValue) / $cfValueStep + 1" | bc)
numberOfRfRunsInFloat=$(echo "scale=2; ($lastRfValue - $firstRfValue) / $rfValueStep + 1" | bc)

numberOfKRunsInInt=${numberOfKRunsInFloat%.*}
numberOfSRunsInInt=${numberOfSRunsInFloat%.*}
numberOfNRunsInInt=${numberOfNRunsInFloat%.*}
numberOfRRunsInInt=${numberOfRRunsInFloat%.*}
numberOfERunsInInt=${numberOfERunsInFloat%.*}
numberOfLRunsInInt=${numberOfLRunsInFloat%.*}
numberOfWRunsInInt=${numberOfWRunsInFloat%.*}
numberOfCfRunsInInt=${numberOfCfRunsInFloat%.*}
numberOfRfRunsInInt=${numberOfRfRunsInFloat%.*}

echo Number of K different values : $numberOfKRunsInInt
echo Number of S different values : $numberOfSRunsInInt
echo Number of N different values : $numberOfNRunsInInt
echo Number of R different values : $numberOfRRunsInInt
echo Number of E different values : $numberOfERunsInInt
echo Number of L different values : $numberOfLRunsInInt
echo Number of W different values : $numberOfWRunsInInt
echo Number of Cf different values : $numberOfCfRunsInInt
echo Number of Rf different values : $numberOfRfRunsInInt
echo Number of iterations for each parameters set : $numberOfIterations

numberOfExperiments=`expr $numberOfKRunsInInt \* $numberOfSRunsInInt \* $numberOfNRunsInInt \* $numberOfRRunsInInt \* $numberOfERunsInInt \* $numberOfLRunsInInt \* $numberOfWRunsInInt \* $numberOfCfRunsInInt \* $numberOfRfRunsInInt \* $numberOfIterations`
currentExperiment=0
for k in $(seq $firstKValue $kValueStep $lastKValue)
do
	for s in $(seq $firstSValue $sValueStep $lastSValue)
	do
		for w in $(seq $firstWValue $wValueStep $lastWValue)
		do
			for n in $(seq $firstNValue $nValueStep $lastNValue)
			do
				for r in $(seq $firstRValue $rValueStep $lastRValue)
				do
					for e in $(seq $firstEValue $eValueStep $lastEValue)
					do
						for l in $(seq $firstLValue $lValueStep $lastLValue)
						do
							for cf in $(seq $firstCfValue $cfValueStep $lastCfValue)
							do
								for rf in $(seq $firstRfValue $rfValueStep $lastRfValue)
								do
									for i in $(seq 1 1 $numberOfIterations)
									do							
										currentExperiment=`expr $currentExperiment + 1`
										echo $currentExperiment/$numberOfExperiments i = $i k = $k s = $s w = $w n = $n r = $r e = $e l = $l cf = $cf rf = $rf
										parameters="_k"$k"_s"$s"_w"$w"_n"$n"_r"$r"_e"$e"_l"$l"_cf"$cf"_rf"$rf"_i"$i
										outputFolderPath=$outputMasterFolder$dataFileName$parameters
										logFilePath=$outputMasterFolder"log_"$dataFileName$parameters.txt
										profilerFile=$outputMasterFolder"log_"$dataFileName$parameters.hprof #-agentlib:hprof=heap=all,file=$profilerFile
										
										java -jar hkplusplus.jar -lgmm -i $inputDataFullPath -o $outputFolderPath -k $k -n $n -r $r -s $s -l $l -e $e -w $w -c -dm -in &> $logFilePath
										if [ $i -gt 1 -a $i -eq $numberOfIterations ]
										then
											#pobiera liczbe linii z pliku
											linesInFile=($(wc -l compactSummaryResults.csv))
											upperBound=`expr $linesInFile - $numberOfIterations + 1`
											lowerBound=`expr $linesInFile`
											echo "min;=min(B$upperBound:B$lowerBound);=min(C$upperBound:C$lowerBound);=min(D$upperBound:D$lowerBound);=min(E$upperBound:E$lowerBound);=min(F$upperBound:F$lowerBound);=min(G$upperBound:G$lowerBound);=min(H$upperBound:H$lowerBound);=min(I$upperBound:I$lowerBound);=min(J$upperBound:J$lowerBound);=min(K$upperBound:K$lowerBound);=min(L$upperBound:L$lowerBound);=min(M$upperBound:M$lowerBound);=min(N$upperBound:N$lowerBound);=min(O$upperBound:O$lowerBound);=min(P$upperBound:P$lowerBound);=min(Q$upperBound:Q$lowerBound);=min(R$upperBound:R$lowerBound);=min(S$upperBound:S$lowerBound);=min(T$upperBound:T$lowerBound);=min(U$upperBound:U$lowerBound);=min(V$upperBound:V$lowerBound);=min(W$upperBound:W$lowerBound);=min(X$upperBound:X$lowerBound);=min(Y$upperBound:Y$lowerBound);=min(Z$upperBound:Z$lowerBound);=min(AA$upperBound:AA$lowerBound);=min(AB$upperBound:AB$lowerBound)" >> compactSummaryResults.csv
											
											echo "max;=max(B$upperBound:B$lowerBound);=max(C$upperBound:C$lowerBound);=max(D$upperBound:D$lowerBound);=max(E$upperBound:E$lowerBound);=max(F$upperBound:F$lowerBound);=max(G$upperBound:G$lowerBound);=max(H$upperBound:H$lowerBound);=max(I$upperBound:I$lowerBound);=max(J$upperBound:J$lowerBound);=max(K$upperBound:K$lowerBound);=max(L$upperBound:L$lowerBound);=max(M$upperBound:M$lowerBound);=max(N$upperBound:N$lowerBound);=max(O$upperBound:O$lowerBound);=max(P$upperBound:P$lowerBound);=max(Q$upperBound:Q$lowerBound);=max(R$upperBound:R$lowerBound);=max(S$upperBound:S$lowerBound);=max(T$upperBound:T$lowerBound);=max(U$upperBound:U$lowerBound);=max(V$upperBound:V$lowerBound);=max(W$upperBound:W$lowerBound);=max(X$upperBound:X$lowerBound);=max(Y$upperBound:Y$lowerBound);=max(Z$upperBound:Z$lowerBound);=max(AA$upperBound:AA$lowerBound);=max(AB$upperBound:AB$lowerBound)" >> compactSummaryResults.csv
											
											echo "average;=average(B$upperBound:B$lowerBound);=average(C$upperBound:C$lowerBound);=average(D$upperBound:D$lowerBound);=average(E$upperBound:E$lowerBound);=average(F$upperBound:F$lowerBound);=average(G$upperBound:G$lowerBound);=average(H$upperBound:H$lowerBound);=average(I$upperBound:I$lowerBound);=average(J$upperBound:J$lowerBound);=average(K$upperBound:K$lowerBound);=average(L$upperBound:L$lowerBound);=average(M$upperBound:M$lowerBound);=average(N$upperBound:N$lowerBound);=average(O$upperBound:O$lowerBound);=average(P$upperBound:P$lowerBound);=average(Q$upperBound:Q$lowerBound);=average(R$upperBound:R$lowerBound);=average(S$upperBound:S$lowerBound);=average(T$upperBound:T$lowerBound);=average(U$upperBound:U$lowerBound);=average(V$upperBound:V$lowerBound);=average(W$upperBound:W$lowerBound);=average(X$upperBound:X$lowerBound);=average(Y$upperBound:Y$lowerBound);=average(Z$upperBound:Z$lowerBound);=average(AA$upperBound:AA$lowerBound);=average(AB$upperBound:AB$lowerBound)" >> compactSummaryResults.csv
											
											echo "stdev;=stdev(B$upperBound:B$lowerBound);=stdev(C$upperBound:C$lowerBound);=stdev(D$upperBound:D$lowerBound);=stdev(E$upperBound:E$lowerBound);=stdev(F$upperBound:F$lowerBound);=stdev(G$upperBound:G$lowerBound);=stdev(H$upperBound:H$lowerBound);=stdev(I$upperBound:I$lowerBound);=stdev(J$upperBound:J$lowerBound);=stdev(K$upperBound:K$lowerBound);=stdev(L$upperBound:L$lowerBound);=stdev(M$upperBound:M$lowerBound);=stdev(N$upperBound:N$lowerBound);=stdev(O$upperBound:O$lowerBound);=stdev(P$upperBound:P$lowerBound);=stdev(Q$upperBound:Q$lowerBound);=stdev(R$upperBound:R$lowerBound);=stdev(S$upperBound:S$lowerBound);=stdev(T$upperBound:T$lowerBound);=stdev(U$upperBound:U$lowerBound);=stdev(V$upperBound:V$lowerBound);=stdev(W$upperBound:W$lowerBound);=stdev(X$upperBound:X$lowerBound);=stdev(Y$upperBound:Y$lowerBound);=stdev(Z$upperBound:Z$lowerBound);=stdev(AA$upperBound:AA$lowerBound);=stdev(AB$upperBound:AB$lowerBound)" >> compactSummaryResults.csv
											echo "" >> compactSummaryResults.csv
											echo "skrot;=average(C$upperBound:C$lowerBound);=stdev(C$upperBound:C$lowerBound);=average(D$upperBound:D$lowerBound);=stdev(D$upperBound:D$lowerBound);=average(E$upperBound:E$lowerBound);=stdev(E$upperBound:E$lowerBound);=average(F$upperBound:F$lowerBound);=stdev(F$upperBound:F$lowerBound);=average(G$upperBound:G$lowerBound);=stdev(G$upperBound:G$lowerBound);=average(H$upperBound:H$lowerBound);=stdev(H$upperBound:H$lowerBound);;;;;;;;;;;;;;;;;;;;skrot;=average(C$upperBound:C$lowerBound);=stdev(C$upperBound:C$lowerBound);=average(D$upperBound:D$lowerBound);=stdev(D$upperBound:D$lowerBound);=average(E$upperBound:E$lowerBound);=stdev(E$upperBound:E$lowerBound);=average(F$upperBound:F$lowerBound);=stdev(F$upperBound:F$lowerBound);=average(G$upperBound:G$lowerBound);=stdev(G$upperBound:G$lowerBound);=average(H$upperBound:H$lowerBound);=stdev(H$upperBound:H$lowerBound);"  >> compactSummaryResults.csv
											echo "" >> compactSummaryResults.csv
											echo "" >> compactSummaryResults.csv
											
										fi
											
										if [ "$currentExperiment" -eq 1 ];
										then
											/home/lolech/Hk++/utils/addbomb.sh compactSummaryResults.csv
										fi
									done
								done
							done
						done
					done		
				done
			done
		done
	done
done
