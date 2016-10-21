cd ./Scrapers
echo $(pwd)
for SCRIPT in *
    do
        if [ -f $SCRIPT -a -x $SCRIPT ]
        then
#            echo $(pwd)
            ./$SCRIPT
        fi
    done
