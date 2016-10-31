cd ./Scrapers
echo $(pwd)
for SCRIPT in *
    do
        if [ -f $SCRIPT -a -x $SCRIPT ]
        then
            ./$SCRIPT 2> ../log/$SCRIPT
        fi
    done
