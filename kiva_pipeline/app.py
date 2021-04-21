from fastapi import FastAPI
import requests

app = FastAPI()

BASE_URL = "https://api.kivaws.org/graphql?query="


@app.get("/")
async def home() -> str:
    return "Hello there!"


@app.get("/get_n_kiva_loans")
def kiva_get(limit_number: int = 5) -> dict:
    query = """
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

    r = requests.post(BASE_URL, json={'query': query, 'variables': variables})

    return r.json()
