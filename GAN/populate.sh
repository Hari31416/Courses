#/bin/bash

echo "Creating new directories"
#take user input for course name
read -p "Enter course name: " course
mkdir $course
mkdir $course/Notes
#take user input for number of weeks and convert to array
read -p "Enter number of weeks: " numWeeks
for week in $(seq 1 $numWeeks); do
    mkdir $course/W$week
    mkdir $course/W$week/Assignments
    mkdir $course/W$week/Labs
done;