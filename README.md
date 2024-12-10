# oalexdump
This project dumps all of the [OpenAlex](https://openalex.org/) database into a containerized Postgresql environment. As of this writing (Dec 10, 2024) this is going to be a one-time setup and NOT a live ETL pipeline.

Required software:
Before you can clone this repo and run the code you need the following installed on your machine:
1. Install Docker. You can get the respective downlaoder for your OS from the [Docker website](https://www.docker.com/products/docker-desktop/).
  - You do NOT have to get the paid version of Docker for this project.
2. 

Here are the steps you need to follow to get the OpenAlex database using this repository:
1. 

Here are the steps I followed in creating this repository:
I followed the OpenAlex documentation. Specifically, the ['Download to your machine' guide](https://docs.openalex.org/download-all-data/download-to-your-machine) first and then the ['Load to your relational database' guide](https://docs.openalex.org/download-all-data/upload-to-your-database/load-to-a-relational-database).

1. I create this repository and cloned it to a local directory. Everything that follows is done with a terminal in that local directory (So `cd` to the directory). 
2. I added an entry in the .gitignore to ignore the folder `openalex_snapshot`. This directory will hold the snapshot OpenAlex provides via s3 as mentioned in the ['Download to your machine' guide](https://docs.openalex.org/download-all-data/download-to-your-machine).
3. I created the `openalex_snapshot` directory in the repository.
4. I installed `awscli` with choco: `choco install awscli`
5. I ran this command as described in [the OpenAlex docs](https://docs.openalex.org/download-all-data/download-to-your-machine): `aws s3 sync "s3://openalex" "./openalex_snapshot" --no-sign-request`
6. 
