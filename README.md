# labsecurity
[![Build Status](https://img.shields.io/github/stars/dylanmeca/labsecurity.svg)](https://github.com/dylanmeca/labsecurity)
[![License](https://img.shields.io/github/license/dylanmeca/labsecurity.svg)](https://github.com/dylanmeca/labsecurity/blob/main/LICENSE)
[![dylanmeca](https://img.shields.io/badge/author-dylanmeca-green.svg)](https://github.com/dylanmeca)
[![bug_report](https://img.shields.io/badge/bug-report-red.svg)](https://github.com/dylanmeca/labsecurity/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
[![security_policy](https://img.shields.io/badge/security-policy-cyan.svg)](https://github.com/meca/labsecurity/blob/main/.github/SECURITY.md)
[![Python](https://img.shields.io/badge/language-Python%20-yellow.svg)](https://www.python.org)
![logo](https://raw.githubusercontent.com/dylanmeca/labsecurity/main/.github/icon.jpg)

labsecurity is a tool that brings together python scripts made for ethical hacking, in a single tool, through a console interface.

# Warning

This software was created for educational purposes, where it is shown how a hacker would access certain information and how to prevent it from happening.

As a labsecurity software developer I will not be held responsible if you use this software for illegal purposes. 

This software was created for ethical hacking and educational purposes.

## What can labsecurity do

* You can get the information from the headers of a website
* You can get the WordPress version although researching also finds the Jekyll version
* You can scan a public ip
* Can scan ports using nmap
* It can do a lot of cool things

## Pre-requirements

The requirements to use the system is to have the following python modules installed:

```text
colorama
requests
python-nmap
wheel
```

## Installation

To install labsecurity on linux run these commands on your Linux Terminal.

```shell

git clone https://github.com/dylanmeca/labsecurity
cd labsecurity
chmod +x *;ls
python3 setup.py install

```

Once done, it begins to install.

to start labsecurity you just have to put the ``` labsecurity ``` command in the terminal.

Ready


## Usage:

To use the labsecurity command you just have to put the ```labsecurity``` command, and once that is done the system console will be loaded.

To obtain information on the commands, you can execute the ```help``` command within the console to obtain information on the main commands. And you can use the ```show options``` command to get information from the other commands.

## Documentation

The project documentation is in: [https://dylanmeca.github.io/labsecurity-documentation](https://dylanmeca.github.io/labsecurity-documentation)

## Authors

* **Dylan Meca** - *Initial Work* - [dylanmeca](https://github.com/dylanmeca)

You can also look at the list of all [contributors](https://github.com/dylanmeca/labsecurity/contributors) who have participated in this project.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/dylanmeca/labsecurity/blob/main/.github/CONTRIBUTING.md) for details of our code of conduct, and the process for submitting pull requests.

## License

The license for this project is [MIT](https://github.com/dylanmeca/labsecurity/blob/main/LICENSE)
