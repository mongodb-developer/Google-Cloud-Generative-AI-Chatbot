# Generative AI Customer Service Chatbot

This is a demo of a customer service chatbot using Generative AI through Google Cloud's Vertex AI PaLM APIs. The app also leverages MongoDB Atlas Search to look for relevant answers in a MongoDB Atlas database. Finally, the app can detect dissatisfied customers with sentiment analysis.

## Quickstart

1. MongoDB Atlas setup
    * Deploy a new MongoDB database cluster in your Atlas account. You can use the free M0 tier for this demo.
    * Create a `XYZ-Corp` database.
    * Create a `Customer` collection in the `XYZ-Corp` database and insert the following document.
      ```json
      {
        "_id":{"$oid":"6488127b353fb41c00a9650b"},
        "customer_id":"111",
        "conversation":[],
        "Name":"Venkatesh Shanbhag"
      } 
      ```
    * Create an `Insurance` collection in the `XYZ-Corp` database and insert the following document.
      ```json
      {
        "_id":{"$oid":"64881424353fb41c00a9650c"},
        "context":"You are a Customer support agent with name Sara working for XYZ-corp.\nIt does provides property Insurance. Sara will not reply for any queries regarding other types of insurance.\nThe company covers insurance of properties like - Hospitals, offices, shops, apartments.\nMax insurance covered will decline over period of time.\nXYZ-Corp only covers Fire and Earthquake hazard insurance. \nYou are allowed to provide only the details regarding the company itself.\nDo not repond with sentiment in any of the responses.",
        "type":"Intro"
      }
      ```
    * Create a `Claims` collection in the `XYZ-Corp` database and insert the following document.
      ```json
      {
        "_id":{"$oid":"64881476353fb41c00a9650d"},
        "claim_number":"12345",
        "Name":"Venkatesh Shanbhag",
        "Claim_amount":{"$numberLong":"10000"},
        "Currency":"USD",
        "Claim_status":"In progress","customer_id":"111"
      }
      ```
    * Create an Atlas Search index with the name `default` on the `Claims` collection using the default settings. Follow the Atlas Search documentation: https://www.mongodb.com/docs/atlas/atlas-search/create-index/

1. Google Cloud setup

    * Set the Google Cloud project name.

      ```commandline
      gcloud config set project <PROJECT_ID>
      ```

    * Clone the repository.

      ```commandline
      git clone https://@github.com/mongodb-developer/gen-ai-chatbot.git
      ```

    * Update the MongoDB Atlas database connection string and the Google Cloud project name in `main.py`.

    * Run the application.

      ```commandline
      python3 main.py
      ```


## Contributors ✨

<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center">
        <a href="https://github.com/theshanbhag">
            <img src="https://media.licdn.com/dms/image/C5603AQGqxMNuhYMt3A/profile-displayphoto-shrink_800_800/0/1611200471754?e=1692230400&v=beta&t=AAEsCZrrjsAC8kAgAbd16GdD0wkoHICCuee9dTkh3uk" width="100px;" alt=""/><br />
            <sub><b>Venkatesh Shanbhag</b></sub>
        </a><br />
    </td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

## Disclaimer

Use at your own risk; not a supported MongoDB product
