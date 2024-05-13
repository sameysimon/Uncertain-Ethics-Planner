#!/bin/bash

ResultsPath="New_Default"

mkdir -p "${ResultsPath}"


for ((i=0; i<6; i++)) do
    for ((j=0; j<5; j++)) do
        python3 -m EthicsPlanner --theories $i --algo "MM_ILAO" --outputFiles "${ResultsPath}/MM_LAO" --weeks 5
    done
done

for ((i=0; i<3; i++)) do
    for ((j=0; j<5; j++)) do
        python3 -m EthicsPlanner --theories $i --algo "SM_ILAO" --outputFiles "${ResultsPath}/SM_LAO" --weeks 5
    done
done

for ((i=0; i<6; i++)) do
    for ((j=0; j<5; j++)) do
        python3 -m EthicsPlanner --theories $i --algo "MM_VI" --outputFiles "${ResultsPath}/MM_VI" --weeks 5
    done
done

for ((i=0; i<3; i++)) do
    for ((j=0; j<5; j++)) do
        python3 -m EthicsPlanner --theories $i --algo "SM_VI" --outputFiles "${ResultsPath}/SM_VI" --weeks 5
    done
done
