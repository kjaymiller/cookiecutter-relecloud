# Cookiecutter Relecloud

# Installing our modified cookiecutter template

If you're running this cookiecutter from the url you will need to import our fork of cookiecutter.

```shell
python -m pip install git+https://github.com/kjaymiller/cookiecutter.git@kjaymiller-adds-_cookiecutter
```

> **Note**
We've submitted our needed changes to the [cookiecutter project](https://github.com/cookiecutter/cookiecutter/issues/1873). This may not be required in the future.

# Deploying your cookiecutter template
- Create a new project
- import [our cookiecutter template](#installing-our-modified-cookiecutter-template)

```
python -m venv venv
source venv/bin/activate
python -m pip install git+https://github.com/kjaymiller/cookiecutter.git@kjaymiller-adds-_cookiecutter
python -m cookiecutter gh:kjaymiller/cookiecutter-relecloud
```

# Running your Deployment via DevContainer/Github Codespaces
This template is designed to work with DevContainers and GitHub Codespaces. You can deploy the Github Codespaces instance by cliking the green code button and creating a new codespace.

To deploy the dev container locally you can do so with a compatible code editor like Visual Studio Code.

# Deploy your template to Azure

These templates are configured to deploy to Microsoft Azure via the Azure Developer CLI. You can deploy your project immediately using `azd up`
