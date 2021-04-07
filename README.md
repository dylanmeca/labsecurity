# lab_tool
[![Build Status](https://img.shields.io/github/stars/dylan14567/lab_tool.svg)](https://github.com/dylan14567/lab_tool)
[![License](https://img.shields.io/github/license/dylan14567/lab_tool.svg)](https://github.com/dylan14567/lab_tool/blob/main/LICENSE)
[![dylan14567](https://img.shields.io/badge/author-dylan14567-green.svg)](https://github.com/dylan14567)
[![bug_report](https://img.shields.io/badge/bug-report-red.svg)](https://github.com/dylan14567/lab_tool/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
[![security_policy](https://img.shields.io/badge/security-policy-cyan.svg)](https://github.com/dylan14567/lab_tool/blob/main/SECURITY.md)
[![Python](https://img.shields.io/badge/language-Python%20-yellow.svg)](https://www.python.org)
![logo](https://raw.githubusercontent.com/dylan14567/lab_tool/main/logo.jpg)

lab_tool is a system that is used for ethical hacking and computer security tests, this system is also a python library.

# Warning

This tool is only for educational purpose.

If you use this tool for other purposes except education we will not be responsible.

## Pre-requirements

The requirements to use the system is to have the following python modules installed:

```
colorama
requests
wheel
```

## Installation

To install lab_tool on linux run these commands on your Linux Terminal.

```shell

git clone https://github.com/dylan14567/lab_tool
cd lab_tool
chmod +x *;ls
python3 setup.py install

```

Once done, it begins to install.

to start lab_tool you just have to put the ``` lab_tool ``` command in the terminal.

Ready


## Usage:

To use the lab_tool command you just have to put the ```lab_tool``` command, and once that is done the system console will be loaded.

Inside the lab tool console place the ``` help ``` command to know more information about how to use the system

## Custom script

If you want to create your own system and your own code using the labtool module you must do the following:

```python 

from labtool.headers import *
from labtool.scanners import *

scanner = scanner ()

header = header ()

scanner.scanports(127.0.0.1) # Scan the ports of an ip
header.headerweb ('http://127.0.0.1') # Gives information from a website

```

## Authors

* **Dylan Alexander** - *Initial Work* - [dylan14567](https://github.com/dylan14567)

You can also look at the list of all [contributors](https://github.com/dylan14567/lab_tool/contributors) who have participated in this project.


## Contributing

Please read [CONTRIBUTING.md](https://github.com/dylan14567/lab_tool/blob/main/CONTRIBUTING.md) for details of our code of conduct, and the process for submitting pull requests.

## License

The license for this project is [MIT](https://github.com/dylan14567/lab_tool/blob/main/LICENSE)

