# Troubleshooting

## non-Python Package dependencies
`Cookiecutter-relecloud` builds instances that include support for [DevContainers](https://containers.dev) and deployments via [Azure CLI](https://aka.ms/azure-cli) or [Azure Developer CLI](https://aka.ms/azd).

You will need to ensure all required products are installed and up to date.

### Installing Dev Containers (VS Code)

If using VS Code you can install Dev Containers using the Dev Containers Extension. You will need docker installed. Alternatively, you can develop inside of a [GitHub Codespaces](https://github.com/features/codespaces) Instance.

### Installing Azure CLI and Updating the Bicep Template

To install the Azure CLI, follow the instructions that best fit your platform at <https://aka.ms/azure-cli>

Azure CLI includes the Bicep CLI you can ensure that it is up to date using the command:

```shell
az bicep upgrade
```

### Install Azure Developer CLI (AZD)
To install the Azure Developer CLI, follow the instructions that best fit your platform at <https://aka.ms/azd>.

You can ensure that it is up to date using the command:

```shell
curl -fsSL https://aka.ms/install-azd.sh | bash
```


