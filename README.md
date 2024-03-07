# Recruitment-Assistant-Tool

Recruiters face a significant challenge in efficiently reviewing a large 
number of resumes to find the best candidates for a specific job opening. 
Manual screening is time-consuming, and there is a need for a more 
automated solution to streamline the hiring process. The goal is to 
develop a Resume Analyzer that, given a job description, can 
automatically analyze and rank resumes, presenting the recruiter with 
the most relevant and qualified candidates. 

This program will analyse all the resumes in HDFS and print the scores for each and display the top 5 resumes.
Based on the intake percentage, the user can modify the code to shortlist top x or x% candidates.

A project developed by C B Ananya, Ayshwarya B, Gayathri Venkatesan.

## Requirements:
Installation of -
python (I have used version 3.11)
pyspark
PyPDF2

hadoop-3.2.1
spark-3.2.4-bin-hadoop3.2

(I have uploaded the documents for installation of Hadoop Distrubuted File System and Spark for windows)

## Steps to run pre-shortlisting

Navigate to the sbin folder of hadoop and start the hadoop nodes and yarn service (command for windows)
```.\start-dfs.cmd```
```.\start-yarn.cmd```

(2 separate cmd prompt windows would open)

Use the command "jps" to see ensure all services have started succesfully. The following 5 should be displayed in the output:
- Datanode
- ResourceManager
- NameNode
- NodeManager
- Jps

After all services are up and running, put all the resumes (PDFs) in the local file system into HDFS using the put command. (Note, all the filenames have to be unique. Hence, it is advised to number all the files with a prefix using a program beforehand).

To create a new directory in hdfs:
```hadoop fs -mkdir \newdirname```

To put files from local file system to HDFS:
```hadoop fs -put "<path_to_localfile>" "<path_to_destination_dir_in_hdfs>"```

## Running the project
Open command prompt and type ```spark-shell```
Press Enter twice.

To run the python file: ```spark-submit resume-shortlisting.py```

You will see the output with the scores of each resume and a final list containing the file names of the top 5 candidates.

You can use the command ```hadoop fs -cp "<source_file_location_in_HDFS>" "<destination_directory_in_HDFS>``` to transfer the shortlisted resumes into another folder in HDFS.

Here's to this project making your life easier. Cheers!



