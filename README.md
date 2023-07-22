# Cookiecutter Relecloud

## Deployment Options

|Feature| Django| FastAPI| Flask|
|---|---|---|---|
|**Deployment**|-|-|-|
|Deploys via AZD|✅|✅|✅|
|Deploys via Terraform|❌|❌|❌|
|Deploys via ACA|✅|✅|✅|
|Deploys with Azure Web App|❌|❌|❌|
|**Databases**|-|-|-|
|Azure ACA Postgres Plugin|❌|❌|❌|
|Azure Cosmos DB (Postgres Adapter)|✅|✅|✅|
|Azure Cosmos DB (MongoDB)|✅|✅|✅|
|Azure Postgres Flexible Server|✅|✅|✅|
|**Azure Add-ons**|-|-|-|
|Azure vNet|❌|❌|❌|
|Azure Secret KeyVault|✅|✅|✅|

## Deploying your cookiecutter template

1. Create a new folder
2. Create a virtual environment 

```
python -m venv venv
source venv/bin/activate
```

2. Install cookiecutter ( >= 2.2.1)

```
python -m pip install cookiecutter
```

3. Generate the project using this template

```
python -m cookiecutter gh:kjaymiller/cookiecutter-relecloud
```

# Running your Deployment via DevContainer/Github Codespaces
This template is designed to work with DevContainers and GitHub Codespaces. You can deploy the Github Codespaces instance by clicking the green code button and creating a new codespace.

To deploy the dev container locally you can do so with a compatible code editor like Visual Studio Code.

# Deploy your template to Azure

These templates are configured to deploy to Microsoft Azure via the Azure Developer CLI. You can deploy your project immediately using `azd up`
