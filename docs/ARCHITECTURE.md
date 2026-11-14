# Labsecurity 2.0 Architecture

```text
Terminal
  |
  v
labsecurity.py ---> LabsecurityConsole 
                           |
        +------------------+-------------------+
        |                  |                   |
   Registry           Typed options        Generator
     |                    |                   |
 manifest.json      set/unset/show      plugin create/import/install
     |                    |
     +-------------> Executor <--------------+
                         |
                    PluginContext
                         |
              plugins/**/plugin.py
```

**Standalone console.** The core does not import any security plugins and runs with an empty `plugins/` directory. Registry enumeration loads only JSON; it does not import Python code until `run` is called or an extended command is explicitly executed. `manifest.json` declares what the core needs: metadata, options, and entrypoints.

**Reload.** `reload` re-discover manifests and discards Python modules loaded into the framework’s own namespaces. Valid option configurations are preserved as long as their type does not change; removed modules are excluded from the interface.

**Isolation.** Import namespaces prevent common name collisions between plugins, but do not provide security isolation or a sandbox. Plugins execute arbitrary Python code within the same process. To publish a future public gallery, signing/verification, permissions, and process isolation should be implemented as a separate project.

**Compatibility.** The eight scripts with actual functionality from the original ZIP file were converted into plugins; the ninth (`show-options.py`) was replaced by the `help` and `show` commands. The originals remain in `legacy/scripts/` for archival purposes. The legacy code importer helps integrate other files with `run(...)`, but does not guarantee universal compatibility.


**Operational security.** No scans are performed when starting, discovering, or generating plugins. Modules that communicate with third-party services (`ipinfo.io`, `viewdns.info`) describe the IP transfer. TCP scans are limited by a port and concurrency cap.
