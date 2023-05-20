# Plugins

While the core functionality (scheduler + UI) is defined in this repo, handlers for different job types should be kept in `plugins/<specific plugin>` directory, e.g. for `HTMLMonitorJob` consumer there is `plugins/serverless-scheduler-html-checker` directory (git submodule).

## How to add a plugin?

1. Add it to the `plugins` directory in root of the repo
2. Modify `plugins-interface` package's `pyproject.toml` so it includes plugin's API package as its dependency (
   you can base on `serverless-scheduler-html-checker-api` usage in there)
3. Run `poetry lock --no-update` in `plugins-interface`
4. Add a directory named `plugins-<your-plugin-name>` in `terraform/deployments/<env>` and copy over `plugins-serverless-scheduler-html-checker`'s `terragrunt.hcl`, modify the copied `terragrunt.hcl` so it points to `terraform/terragrunt.hcl` in the root directory of the plugin
5. Run `utils/complete_build.sh` to prepare the packages to be uploaded
6. Run `utils_complete_deploy.sh` (with proper options for your env) to deploy the app with new plugin support

## Structure of a plugin

The plugins are expected to follow common project structure, so they work seamlessly with existing build system.
Namely:

1. Plugin defines `bin/package_lambda_entrypoint` script, that outputs the zip generated for a project to `.packaging/result/lambda.zip` file (in plugin's root directory). It's up to the developer to define if this script will rely on `serverless-scheduler`'s build system that's used for core packages or define their own logic.
2. Plugin defines `terraform` directory, that contains all the logic needed to deploy the functionality.
   The following variables should be accepted:

- `aws_region` - in what region to deploy
- `service` - to be used in tags as 'Service'
- `stage` - to be used in tags as 'Stage'
- `prefix` - what value to prefix the deployed objects' names with
- `lambda_zip_path` - path to zip file that should be used by the consumer Lambda (build system will automatically insert the zip built in step 1.)
- `distribution_sns_topic_arn` - ARN of the SNS topic that deployment should monitor for incoming events with matching job_type
- `common_layer_arn` - (optional support) ARN of the Lambda layer with `common` package. This is really only usable with Python based plugins
- `plugins_layer_arn` - (optional support) ARN of the Lambda layer with `plugins-interface` package. This is really only usable with Python based plugins

3. Plugin's directory contains a `<plugin-name>-api` python package that exports package following `serverless-scheduler-<>-api` naming scheme and contains `plugin_export` subpackage, which exports:

- `ENUM_MAPPING` - dict from `str` to `str`, keys are ENUM identifiers, while values are string identifiers, e.g. `HTMLMonitorJob`: `html_monitor_job`
- `CLASS_MAPPING` - dict from `str` to `class`, keys are string identifiers (values from `ENUM_MAPPING`), while values are classes that map to a jobType

The reference implementation can be seen in previously mentioned `plugins/serverless-scheduler-html-checker`.
`serverless-scheduler-plugin-example` can be treated as an example of just the API part, even though there's no real logic defined in it.

It's up to the user to define if the consumer should use SQS as a "buffer" before consuming the event by Lambda or not.
In practice the consumer doesn't even have to be a Lambda function, although it's recommended for keeping the whole model serverless.

Installed plugins have access to the `common` layer (via the ARN provided), but they don't have access to `plugins` layer.
The reasoning here is that a scope of a plugin should be completely covered by the single plugin.
