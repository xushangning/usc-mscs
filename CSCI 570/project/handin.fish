set STUDENT_IDS 1234567890_1234567890_1234567890
if string length $argv[1] &> /dev/null
    set STUDENT_IDS $argv[1]
end

mkdir $STUDENT_IDS
cp CPUPlot.png MemoryPlot.png Summary.txt workbench.ipynb $STUDENT_IDS
for f in *.py
    set new_name {$STUDENT_IDS}_$f
    cp $f $STUDENT_IDS/$new_name
    echo "#!/bin/sh

python3 $new_name input.txt" > (string replace 'py' 'sh' $STUDENT_IDS/$new_name)
end

zip -r $STUDENT_IDS $STUDENT_IDS
rm -r $STUDENT_IDS
