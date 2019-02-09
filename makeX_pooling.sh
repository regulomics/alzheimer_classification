#!/bin/bash

. job_pool.sh

: '
See readme.txt for input, output and possible options.
'

function make(){

	echo "running makeX.py for chr $1"
	python3 makeX.py -chr $1 -indir $2 -outdir $3
	echo "X matrix for chr $1 done!"

}

chr=0
all=0
from=1
to=24
indir='./'
outdir='./'

while [[ "$1" != "" ]]; do
        case $1 in

        -chr | -c )             shift
                                chr=$1
                                ;;
        -all | -a )             all=1
                                ;;
        -from )                 shift
                                all=1
                                from=$1
                                ;;
        -to )                   shift
                                all=1
                                to=$1
                                ;;
        -indir )                shift
                                indir=$1
                                ;;
        -outdir )               shift
                                outdir=$1
                                ;;
        *)                      usage
                                exit 1
    esac
    shift
done

if [[ ${all} -eq 1 ]]; then
        job_pool_init $((to-from+1)) 0

        for (( i=$from; i<=$to; i++ )); do                

                job_pool_run make ${i} ${indir} ${outdir}

        done

        job_pool_shutdown
        echo "job_pool_nerrors: ${job_pool_nerrors}"
else
        make ${chr} ${indir} ${outdir}
fi