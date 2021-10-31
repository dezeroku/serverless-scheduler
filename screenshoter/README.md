### Security
The built container needs to be run with (the `chromium.json` file is kept in the same directory as the README.md)
```
--security-opt seccomp=chromium.json
```
to allow it to use some kernel-level functions, which are needed for the sandbox feature to work correctly.
Allowing a bit of kernel-level access still seems to be a better idea than running with no sandboxing at all.
