# LABSECURITY 2.0
[![Starts](https://img.shields.io/github/stars/dylanmeca/labsecurity.svg)](https://github.com/dylanmeca/labsecurity)
[![License](https://img.shields.io/github/license/dylanmeca/labsecurity.svg)](https://github.com/dylanmeca/labsecurity/blob/main/LICENSE)

Labsecurity is a pentesting framework that brings together tools and allows users to create, manage, and run hacking scripts from a single platform, facilitating the automation of cybersecurity testing.

## 📚 Requirements

- Python **3.10 or later**.
- For Nmap plugins, install **Nmap** (the system executable) and `python-nmap`. These are not required to start the console or to perform a simple scan using sockets.

### ⬇️ Installation
To install and use labsecurity, follow these steps:

1. Make sure you have installed [Python](https://www.python.org/) in your system.
2. Download or clone this repository to your computer.
3. Open a terminal and access the repository directory.
4. Run the following command to install the necessary dependencies: ```pip3 install -r requirements.txt```
5. Run the following command to start labsecurity: ```python3 labsecurity.py```

```text
labsecurity > help
labsecurity > search scanport
labsecurity > use auxiliary/scanner/scanport
labsecurity (auxiliary/scanner/scanport) > show options
labsecurity (auxiliary/scanner/scanport) > set RHOSTS 127.0.0.1
labsecurity (auxiliary/scanner/scanport) > set RPORT 8000
labsecurity (auxiliary/scanner/scanport) > run
labsecurity (auxiliary/scanner/scanport) > back
labsecurity > exit
```

## 🔧 Create Your Own Plugin

From the console:

```text
labsecurity > plugin create my_tool
[+] Plugin scaffold generated: plugins/auxiliary/custom/my_tool
```

You can also specify the type and category:

```text
labsecurity > plugin create port_check auxiliary scanner
```

The generator creates the package with:

```text
plugins/auxiliary/custom/my_tool/
  __init__.py
  manifest.json
  plugin.py
```

Open `plugin.py` and replace the `TODO` comment with your logic in the `run(ctx)` function. Adjust the manifest options and run `reload` if you were already using the console. Discovery occurs **without executing the plugin’s code**; loading takes place when you call `run` or a command added by a plugin.

**Basic API:** `ctx.get(“TARGET”)`, `ctx.info(“...”)`, `ctx.success(“...”)`, `ctx.warning(“...”)`, `ctx.error(“...”)`, and `ctx.print(“...”)`. Options can be of type `string`, `integer`, `port`, `boolean`, `url`, or `choice`; `required`, `default`, and `description` are configurable.

## 👷 Contributions
This project is open source and we are open to any kind of contribution. If you want to collaborate with the project, follow these steps:

- Fork this repository.
- Create a branch with your contribution.
- Make a pull request to this repository. 

Be sure to include a detailed description of your contribution and to follow our code standards.

## 🧾 Credits
This project has been developed by [Dylan Meca](https://github.com/dylanmeca) and contributions from [users](https://github.com/dylanmeca/labsecurity/contributors).
