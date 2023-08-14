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

## Testing

### Creating Tests
We have two sets of tests:
1. Generation tests - Tests that verify project generation is accurate
2. Application tests - Tests that are created by cookiecutter that are ran by the generated project

Both sets of tests are created using [Pytest](https://pytest.org).

### Generation tests

The generation tests are located at `/tests/` 

Generation tests use [pytest-cookies](https://github.com/hackebrot/pytest-cookies) to generate an iteration of each project and run a series of tests.

You'll need to include the fixture `bakery` in your new tests to ensure that the desired outcome is happening across all of the products.

```python
def tests_something_happened(bakery, context)
```

### Application tests

Application tests are in `{{cookiecutter.__src_folder_name}}/tests/`.

Application tests use [playwright](https://playwright.dev/python/) and [pytest-playwright](https://github.com/microsoft/playwright-pytest). If you're testing the generated projects, you'll need to have `playwright` installed with dependencies.

```sh
playwright install --with-deps
```


### Running Tests

Our goal is to ensure that the template is always up to date with the latest versions of the tools we use. Tests are run using [GitHub Actions](https://github.com/kjaymiller/cookiecutter-relecloud/actions). You should also run the tests locally before submitting a PR.

There are plenty of tests our repo. The majority of tests are focused on testing deployment scendarios. These cannot be tested without creating a subprocess. These tests are relatively slow and should not be ran on every commit. Instead, they are ran when a PR is submitted.
