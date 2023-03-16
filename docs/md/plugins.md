# How to add a plugin?

1. Add it to the `plugins` directory in root of the repo
2. Modify `plugins-interface` package's `pyproject.toml` so it includes plugin's API package as its dependency (
   you can base on `serverless-scheduler-html-checker-api` usage in there)
3. Run `poetry lock --no-update` in `plugins-interface`
4. Add a directory named `plugins-<your-plugin-name>` in `terraform/deployments/<env>` and copy over `plugins-serverless-scheduler-html-checker`'s `terragrunt.hcl`, modify the copied `terragrunt.hcl` so it points to `terraform/terragrunt.hcl` in the root directory of the plugin
5. Run `utils/complete_build.sh` to prepare the packages to be uploaded
6. Run `utils_complete_deploy.sh` (with proper options for your env) to deploy the app with new plugin support
