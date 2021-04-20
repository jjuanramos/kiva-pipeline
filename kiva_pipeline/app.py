from flask import Flask
import requests

app = Flask(__name__)

BASE_URL = "https://api.kivaws.org/graphql?query="


@app.route("/")
def home() -> str:
    return "Maria BITCH"


@app.route("/kiva")
def kiva_get() -> dict:
    graphql_query = """
        {
            lend {
                loans(sortBy: newest, limit: 5) {
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
    r = requests.get(BASE_URL+graphql_query)
    return r.json()


if __name__ == "__main__":
    app.run()
