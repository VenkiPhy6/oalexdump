# oalexdump

Dec 10, 2024

This project dumps all of the [OpenAlex](https://openalex.org/) database into a containerized Postgresql environment. As of this writing, this is going to be a one-time setup and NOT a live ETL pipeline.

## Required hardware

Please be aware of the space constraints here. You will need at least 2TB. As of the day of this writing, you will require 453GB to download the snapshot data, 213 GB to store the flattened csv files, and ~1.5 TB to store the Postgre database. You will also need a decent RAM (I recommend 16GB) for flattening the JSON files to csv files in memory. Optionally, you may need a multicore processor if you want to speed things up by parallelizing the scripts.

## Required software
Before you can clone this repo and run the code you need to:

1. install Docker in your machine. You can get the respective downloader for your OS from the [Docker website](https://www.docker.com/products/docker-desktop/). Note that you do NOT have to get the paid version of Docker for this project.
2. install the AWS Command Line Interface, `awscli`. Installer can be found on [AWS website](https://aws.amazon.com/cli/).
	- You do NOT need an AWS account for this!

## Steps to use this repository
1. Clone this repository into your local machine at a location of your choice.
2. Open a terminal, `cd` into the repository. All the other commands must be run in such a terminal.
3. In the terminal from previous step, run `aws s3 sync "s3://openalex" "./openalex_snapshot" --no-sign-request`. This will take a while to download based on your internet speed. Wait for it to finish.
4. In the terminal from previous step, run `docker-compose build`
	- This command uses the configuration specified in `Dockerfile` and the `docker-compose.yml` to install the latest postgre image from Docker with a specific username, password and database name. It then also installs Python 3 inside this Postgre image. The data you will put into the Postgre database is persisted by binding it to the `postgres_data` folder. You can open a terminal into the container and run all the python scripts in the `scripts` of this repository and access the files in the `openalex_snapshot` and `csv_files` folders.
5. In the terminal from previous step, run `docker-compose up -d`. 
	- Now two Docker containers should be up and running. One is the PostgreSQL container (called `postgres-python-container`) and another is the Python container (called `python-scripts-container`) with the necessary packages installed.
6. In the terminal from the previous step, run `docker exec -it python-scripts-container /bin/bash`
	- This creates an interactive terminal to the Python container.
 	- If you are running into errors in this step, you may want to make sure that the Docker containers are running. Run `docker ps` and see if the two containers are up and running. If not, see previous step.
7. In the Docker terminal from previous step, run `psql -h postgres -d openalex -U oalexer` and type the passwrod specified in the Dockerfile (by default it is: alexandria).
8. In the Docker terminal from previous step, run `\i scripts/00_openalex-pg-schema.sql`
	- This script will create a set of tables that matches the schema [shown in the docs](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database/postgres-schema-diagram).
	- Please read step 1 of the [documentation from OpenAlex](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database#step-1-create-the-schema).
9. In the Docker terminal from previous step, run `python3 ./scripts/01_flatten-openalex-jsonl.py`
	- This script will take the json files from `openalex_snapshot` folder, turn it into compressed csv files, and put them in the `csv_files` folder.
 	- This take quite a while to run. So be patient. If you are in a hurry, you may want to parallelize the script or simply split the script into multiple parts and run them all simultaneously.
 	- Please read step 2 of the [documentation from OpenAlex](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database#step-2-convert-the-json-lines-files-to-csv)
10. In the Docker terminal from the previous step, run `\i scripts/02_copy-openalex-csv.sql`
	- Please read step 3 of the [documentation from OpenAlex](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database#step-3-load-the-csv-files-to-the-database)
 	- For me this was by far the most time consuming step! It all depends on the read/write speeds of your HDD/SSD. If you are in a hurry, I'd recommend prioritizing the tables you are most interested in by editing the `02_copy-openalex-csv.sql` script to put the priority tables up top. That way, as soon as your top tables are done, you can do some analysis while the rest of the tables continue to load.

You are done! As an optional step, create more indices as you see fit to speed up your specific query. 

## Note to self
As a note-to-self, I also write down the steps I followed in creating this repository:
I followed the OpenAlex documentation. Specifically, the ['Download to your machine' guide](https://docs.openalex.org/download-all-data/download-to-your-machine) first and then the ['Load to your relational database' guide](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database).

1. I created this repository and cloned it to a local directory. Everything that follows was done with a terminal in that local directory (So `cd` to the directory). 
2. I added an entry in the .gitignore to ignore the folder `openalex_snapshot`. This directory will hold the snapshot OpenAlex provides via s3 as mentioned in the ['Download to your machine' guide](https://docs.openalex.org/download-all-data/download-to-your-machine).
3. I created the `openalex_snapshot` directory in the repository.
4. I installed `awscli` with chocolatey: `choco install awscli`
5. I ran this command as described in [the OpenAlex docs](https://docs.openalex.org/download-all-data/download-to-your-machine): `aws s3 sync "s3://openalex" "./openalex_snapshot" --no-sign-request`
6. I added an entry in the .gitignore to ignore the folders `postgres_data` and `csv_files`.
7. I created the `postgres_data`  and `csv_files` directory in the repository.
8. I created the `scripts` directory in the repository.
9. I built the Docker container and ran it.
	1. I wrote up a Dockerfile and a docker-compose.yml. You can read them to understand the config.
	2. I did `docker-compose build` and `docker-compose up -d` 
10. I then ran the rest of the scripts provided in the ['Load to your relational database' guide](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database) within the Docker container.
	- I tried creating one Python script to orchestrate all the scripts at once but gave up after running into trouble with the copy commands! If you're mood, please do it and give me a pull request.
 	- At the end, I skipped loading some of the tables into the database since it was taking too long and I didn't see the need to have that data.
