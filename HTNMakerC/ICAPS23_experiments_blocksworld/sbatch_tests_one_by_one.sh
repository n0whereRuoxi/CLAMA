#!/bin/sh
Domains=("blocksworld")
Prec=("false")
Prune=("false")
Curriculum=("_curriculum" "_original")
for domain in ${Domains[@]}
do
    for curriculum in ${Curriculum[@]}
    do
        for prune in ${Prune[@]}
        do
            if [ $prune = "true" ]
            then
                prune="_prune"
            else
                prune=""
            fi
            for prec in ${Prec[@]}
            do            
                if [ $prec = "true" ]
                then
                    prec="_prec"
                else
                    prec=""
                fi
                for num in {2..25}
                do
                    for count in {0..49}
                    do
                        fname="/scratch/zt1/project/nau-lab/user/rli12314/HTNTeacher/ICAPS23_experiments_${domain}/scripts/run_verification_${domain}${curriculum}${prune}${prec}_${num}_${count}.bash"
                        sbatch -n 1 -N 1 -t 00:10:00 $fname
                    done
                    echo $domain $curriculum $prune $prec
                done
            done
        done
    done
done