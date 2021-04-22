from fastapi import FastAPI
import requests

app = FastAPI()

BASE_URL = "https://api.kivaws.org/graphql?query="


@app.get("/")
def home() -> tuple:
    return "Hello there!", 200


@app.get("/get_kiva_batch")
def reroute_batch() -> dict:
    return {
        "message": "You need to provide a number such as /get_kiva_batch/2"
    }


@app.get("/get_kiva_batch/{limit_number}")
def get_kiva_batch(limit_number: int = 5) -> dict:
    batch_query = """
        query ($limit_number: Int)
        {
            lend {
                loans(sortBy: newest, limit: $limit_number) {
                    values {
                        id
                        loanAmount
                        status
                        researchScore
                        repaymentInterval
                        endorser {
                            id
                        }
                        distributionModel
                        terms {
                            currencyFullName
                            disbursalAmount
                            disbursalDate
                            flexibleFundraisingEnabled
                        }
                        loanAmount
                        paidAmount
                    }
                }
            }
        }
    """

    if limit_number > 20:
        limit_number = 20

    variables = {
        "limit_number": limit_number
    }

    r = requests.post(
        BASE_URL,
        json={
            "query": batch_query,
            "variables": variables
        }
    )

    return r.json()


@app.get("/get_kiva_item")
def reroute_item() -> dict:
    return {
        "message": "You need to provide an id such as /get_kiva_item/50000"
    }


@app.get("/get_kiva_item/{id}")
def get_kiva_item(id: int) -> dict:
    item_query = """
        query($id: Int!)
        {
            lend {
                loan(id: $id) {
                id
                loanAmount
                status
                researchScore
                repaymentInterval
                endorser {
                    id
                }
                distributionModel
                terms {
                    currencyFullName
                    disbursalAmount
                    disbursalDate
                    flexibleFundraisingEnabled
                }
                loanAmount
                paidAmount
                }
            }
        }
    """

    variables = {
        "id": id
    }

    r = requests.post(
        BASE_URL,
        json={
            "query": item_query,
            "variables": variables
        }
    )

    return r.json()
