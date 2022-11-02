# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |

| *Function App*                 |    Premium      |  $155.27          |
| *APP Service *                 |    Standard     |  $73.00           |
| *Storage Accounts*             |    Premium      |  $150.69          |
|*Azure Postgres Database*       |    General      |  $368.19          |
| *Azure Service Bus*            |   Standard      |$9.81              |

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

Azure App Service is a powerful web application hosting platform. 

An App Service provides a detailed view of application health and performance to make right decisions for business improvement. It also provides deep insights into app’s response times CPU & memory utilization, throughput and error trends.

Appservice provides layered security like multi-factor authentication to access the application. Azure App Service is also ISO and PCI compliant. Apps can be hosted anywhere manually or automatically on Microsoft’s global datacenter infrastructure. App Service provides high availability with of 99.5% SLA uptime.

Microsoft Azure offers pay-as-you-go pricing. It is very cost effective for small and medium enterprises. App Services also has built-in load balancers that help save infrastructure costs.

Some Disadvantages:

No remote Deskstop, Performent counter, requirement specific skillset with admintrator

--------------------

Azure Functions is a serverless solution that allows you to write less code, maintain less infrastructure, and save on costs. Instead of worrying about deploying and maintaining servers, the cloud infrastructure provides all the up-to-date resources needed to keep your applications running.

It can enables you to easily build serverless and event-driven compute workloads. 
An Azure function can be triggered by an external event. It will executes the code that is implemeted in the function. 

Some Disadvantages:

It is not a replacement for Web APIs. However, in some instances, they are excellent Web API extensions.
Since it is a compute-on-demand service, it is not best for intensive computing and long-running functions.
Designed to execute a single or few things as fast as possible, it can’t perform multiple tasks.


------------------------
Pros of fully-managed PostgreSQL in Azure:
Fully managed high availability, backup, patching and updates. Most ongoing maintenance efforts are taken care of as part of the managed service.
Automated scalability.
Storage is an integrated part of the service, and scales automatically based on usage up to 4TB. Note that you cannot scale down storage.

Cons of fully-managed PostgreSQL in Azure:
Azure SQL Database for PostgreSQL only supports PostgreSQL 9.5, 9.6, 10, and 11. The Flexible Server solution has more limited version support - only PostgreSQL versions 11 and 12. If you run workloads on versions earlier than 9.5, you will need to upgrade your database.

Migration between major versions of PostgreSQL is not supported - you will need to take a dump of the database and restore it to an instance with the new version.
-----------------------
This App is lightweight, therefore deployed through an App Service are reasonable and no need significant compute capability. Function App support microsverices as well as run background job by ServiceBus very good.

This App is lightweight, therefore deployed through an App Service are reasonable and no need significant compute capability.
