# 🛡️ Labsecurity 🐍
[![Build Status](https://img.shields.io/github/stars/dylanmeca/labsecurity.svg)](https://github.com/dylanmeca/labsecurity)
[![License](https://img.shields.io/github/license/dylanmeca/labsecurity.svg)](https://github.com/dylanmeca/labsecurity/blob/main/LICENSE)
[![dylanmeca](https://img.shields.io/badge/author-dylanmeca-green.svg)](https://github.com/dylanmeca)
[![bug_report](https://img.shields.io/badge/bug-report-red.svg)](https://github.com/dylanmeca/labsecurity/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
[![security_policy](https://img.shields.io/badge/security-policy-cyan.svg)](https://github.com/meca/labsecurity/blob/main/.github/SECURITY.md)
[![Python](https://img.shields.io/badge/language-Python%20-yellow.svg)](https://www.python.org)
![labsecurity](https://github.com/dylanmeca/labsecurity/raw/main/presentation.png)

Labsecurity is a tool that bundles ethical hacking python scripts into a single tool with cli interface.

## ⬇️ Installation
To install and use labsecurity, follow these steps:

1. Make sure you have installed [Python](https://www.python.org/) in your system.
2. Download or clone this repository to your computer.
3. Open a terminal and access the repository directory.
4. Run the following command to install the necessary dependencies: ```pip3 install -r requirements.txt```
5. Run the following command to start labsecurity: ```python3 labsecurity.py --help ```

```txt
usage: labsecurity.py [-h] -t TARGET [-p PORT] script_name

Labsecurity is a tool that bundles ethical hacking python scripts into a single tool with cli interface.

positional arguments:
  script_name           Script name to be executed

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Objective to use
  -p PORT, --port PORT  Port to user
```

## 📚 Use

To use this tool you must learn the following concept:

```shell
python3 labsecurity.py -t http://example.com scanweb.py
```
 
By using the ```-t``` parameter I specify the target which in this case is ```http://example.com``` and by putting ```scanweb.py``` at the end I specify the script to be executed. The scripts are located in the ```/scripts``` folder and can be used in the tool.

Another example would be using another script that in this case will be ```scanport.py```:

```shell
python3 labsecurity.py -t 192.168.0.107 -p 80 scanport.py
```

In this case, apart from the ```-t``` parameter, the ```-p``` parameter is added to specify the port and at the end the ```scanport.py``` script is used to scan said port.

You can see the available scripts and their function with the following command:

```shell
python3 labsecurity.py show-options.py
```

## 💻 What can labsecurity do?
Some examples of what this tool can do are:

* You can get the information from the headers of a website
* You can get the WordPress version although by investigating you can also find the Jekyll version
* You can scan a public ip
* Can scan ports using nmap

## 👷 Contributions
This project is open source and we are open to any kind of contribution. If you want to collaborate with the project, follow these steps:

- Fork this repository.
- Create a branch with your contribution.
- Make a pull request to this repository. 

Be sure to include a detailed description of your contribution and to follow our code standards.

## 📜 License
This project is released under the [MIT](https://github.com/dylanmeca/labsecurity/blob/main/LICENSE) license. This means that the code and documentation in this project are free to use, modify, and distribute as long as you respect the license terms.

For more information about the license, see the [LICENSE](https://github.com/dylanmeca/labsecurity/blob/main/LICENSE) file included in this repository.

## 🧾 Credits
This project has been developed by [Dylan Meca](https://github.com/dylanmeca) and contributions from [users](https://github.com/dylanmeca/labsecurity/contributors).
