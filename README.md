# Summary

This project reads the data from <b>Get Coin History API</b> for the bitcoin id: 1 currently and parses the data into 2 different JSON schemas and the same can be accessed by hitting 2 different REST Endpoints.
Project can be easily extended to support multiple coins and multiple timeframes if needed.
Developer documentation for the Source Get Coin History API is available here (https://developers.coinranking.com/api/v1/documentation/coins#get-coin-history)

## Different Tech Stacks

Following Tech Stacks are used in this project
   1. Python
   2. Serverless Framework
   3. Flask  

**Why serverless**

Serverless Framework is a free and open source web framework written using Node.js. More info available [here] (https://www.serverless.com/). Framework is chosen to provision resources on cloud and manage the deployment.

## Getting Started

In order to run this application on local follow the below steps.

Steps outlined assumes that python3, node and npm is already installed and available in the machine.

1. <b> Install serverless</b>: npm install -g serverless
2. <b> Install serverless plugins</b>:  
        npm install --save-dev serverless-wsgi serverless-python-requirements
3. <b> Install serverless-wsgi plugin</b>: sls plugin install -n serverless-wsgi


## Local Development
Run following command to run the API's on local

    sls wsgi serve

After command execution, you will notice the application running on port 5000 and different API's can be accessed using the following URL.

Bitcoin Data API : http://localhost:5000/history/bitcoin-data

Bitcoin Stats API : http://localhost:5000/history/bitcoin-stats

In order to run the app on different port use the below command 
    
    sls wsgi serve -p <port>

## AWS Deployment

In order to deploy to AWS lambda/API Gateway you need to have docker instance running on your machine and also aws cli.

Configure your aws profile by editing the file <b>~/.aws/credentials</b> with your access and secret keys and update serverless.yml provider section with the profile name from the credentials file.

Run the following command

**sls deploy**

you will notice the docker command will take time to create the image and then it will be deployed to aws by serverless using cloudformation templates.

## API Schemas:
 1. Bitcoin Data API returns the JSON Array having following schema and can be accessed by <b>/history/bitcoin-data</b>

        {
            "date": "{date}",
            "price": "{value}",
            "direction": "{up/down/same}",
            "change": "{amount}",
            "dayOfWeek": "{name}”,
            "highSinceStart": "{true/false}”,
            "lowSinceStart": "{true/false}”
        }


 2. Bitcoin Stats API returns the JSON Array having following schema and can be accessed by <b>/history/bitcoin-stats</b>

        {
            "date": "{date}",
            "price": "{value}",
            "dailyAverage": "{value}",
            "dailyVariance": "{value}",
            "volatilityAlert:": "{true/false}"
        }




