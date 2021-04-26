# Kiva Pipelines

The purpose of this project is to write an API that retrieves data from another api given an id and returns it. We will write this API in different languages to see how they compare. The requirements of this API are:

- It has to have an endpoint /get_kiva_item
- It has to be containerized in order to run inside GCP Cloud Run
- It has to be asynchronous
- It has to be tested locally

We have chosen to use the API that [Kiva](https://www.kiva.org/build) provides, as it is a well designed GraphQL API.

For the python version of this project, we have used [Poetry](https://python-poetry.org/) as package manager. If you have Poetry installed, all you need to do is:

1. `git clone https://github.com/jjuanramos/kiva-pipeline.git`
2. `poetry install`
3. `poetry run uvicorn kiva_pipeline.app:app --reload`
4. You will have the app listening at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

If you don't have Poetry installed, you can use this app by using Docker. The steps would be:

1. `git clone https://github.com/jjuanramos/kiva-pipeline.git`
2. `docker build . --tag kiva_pipeline`
3. `docker run -d --name kiva_pipeline_container -p 80:80 kiva_pipeline`
4. You will have the app listening at [http://0.0.0.0/](http://0.0.0.0/)