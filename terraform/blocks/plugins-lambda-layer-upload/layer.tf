resource "aws_lambda_layer_version" "plugin_layer" {
  filename   = var.layer_zip_path
  layer_name = "${var.prefix}-plugin-layer"

  description         = "Plugin Lambda layer to be shared between Python microservices of ${var.prefix}. It provides definitions from plugins"
  compatible_runtimes = ["python3.9"]
  source_code_hash    = filebase64sha256(var.layer_zip_path)

  # If set to true, creating a new layer version won't delete the old versions
  # Also complete `destroy` on the resources will keep the layers dangling.
  # Note that setting this to false doesn't break existing Lambda deployments when
  # new layer version is uploaded. They will still have the access to the old one.
  skip_destroy = var.keep_old_layers
}
