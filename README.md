![alt text](readmefiles\lucksmall.png)

<h1 align="center">Planner Data Publisher</h1>

<h2 align="left">Project Description</h2>

Python Azure function for publishing Microsoft Planner data into Azure blob storage. 

<h2 align="left">How to Run Locally</h2>

1. Install Visual Studio Code and ensure you have the Azure Functions Extension Installed 
2. Clone this Repository 
3. Open folder location where you cloned repo. The .vscode project folder will import the project settings for you
4. You will be prompted to created a Python Virtual Environment with a click of a button for project to run on
5. From the tool bar Run -> Start Debugging will run the function locally 

Note that this function app requires a functional account due to the Planner API requiring [Delegated Permissions](https://docs.microsoft.com/en-us/graph/auth/auth-concepts#delegated-and-application-permissions). It also requires a Blob Storage & Access Key to land Planner Data into. 

All of these configuration keys/secrets are set inside of local.settings.json


<h2 align="left">How to Contribute</h2>

To contribute to this Repository branch off of Main and name the branch to include your name and short description of work you are doing. Once your work has been completed you may begin a merge request into Main. 


<h2 align="left">Built With</h2>

- Python 3.7
- Visual Studio Code 
- Azure Functions 

Python Packages

- requests 
- azure-storage-file-datalake
- pytz


<h2 align="left">Author</h2>

Nicholas Peterson 

Data Engineer  :sunglasses:

Nick.Peterson@luckcompanies.com  :four_leaf_clover: