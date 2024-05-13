#!/bin/bash

mkdir -p "Horizon_Results"

for ((h=3; h<20; h++)) do
    for ((i=0; i<6; i++)) do
        for ((j=0; j<5; j++)) do
            python3 -m EthicsPlanner --theories $i --algo 'MM_ILAO' --outputFiles 'Horizon_Results/MM_ILAO' --weeks $h
        done
    done
done
