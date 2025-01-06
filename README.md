# oalexdump

Dec 10, 2024

This project dumps all of the [OpenAlex](https://openalex.org/) database into a containerized Postgresql environment. As of this writing, this is going to be a one-time setup and NOT a live ETL pipeline.

Required software:
Before you can clone this repo and run the code you need the following installed on your machine:
1. Install Docker. You can get the respective downloader for your OS from the [Docker website](https://www.docker.com/products/docker-desktop/).
  - You do NOT have to get the paid version of Docker for this project.
2. 

Here are the steps you need to follow to get the OpenAlex database using this repository:
1. Clone this repository into your local machine at a location of your choice.
	- Hope you are aware of the space constraints here. As of the day of this writing, you will require 453GB to download the snapshot data (step 5). Then another x GB to store the flattened csv files. Then another x GB to store the Postgre database. I used a 4TB hard drive to do all this.
2. In your local version of the repository, create 3 directories: 
	- `openalex_snapshot`
	- `postgres_data`
	- `csv_files`
3. Open a terminal, `cd` into the repository. All the other commands must be run in such a terminal.
4. Install the AWS Command Line Interface, `awscli`. Installer can be found on [AWS website](https://aws.amazon.com/cli/).
	- You do NOT need an AWS account for this!
5. In the terminal from step 3, run `aws s3 sync "s3://openalex" "./openalex_snapshot" --no-sign-request`
6. In the terminal from step 3, run `docker-compose build`
	- If you get a git commit related warning, please ignore.
7. In the terminal from step 3, run `docker-compose up -d`. 
	- Now two Docker containers should be up and running. One is the PostgreSQL container and another is the Python container with the necessary packages installed.
8. You now need to create an interactive terminal to the Python container. Run `docker exec -it python-scripts-container /bin/bash`
	- You may want to make sure the Docker containers are running. Run `docker ps` and see if the two containers are up and running. If not, see step 7.
9. In the terminal from step 8, run `python3 ./scripts/00_setupdb.py`	
10. If step 9 is successful, in the same terminal, run `python3 ./scripts/flatten-openalex-jsonl.py`
	- Now wait - for a long time!	


Here are the steps I followed in creating this repository:
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
10. I ran some Python scripts.
	1. I wrote `00_setupdb.py` to run the SQL commands from the `openalex-pg-schema.sql` file obtained [from the URL](https://github.com/ourresearch/openalex-documentation-scripts/blob/main/openalex-pg-schema.sql) mentioned in the docs. It is run on the PostGre containerized in the Docker.
	2. I then run the `flatten-openalex-jsonl.py` script obtained [from the URL](https://github.com/ourresearch/openalex-documentation-scripts/blob/main/flatten-openalex-jsonl.py) mentioned in the docs.
		- I didn't have the mood to parallelize things as the docs suggested. But you are welcome to do so.