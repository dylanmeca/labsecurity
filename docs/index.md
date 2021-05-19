---
layout: default
title: labsecurity
description: labsecurity is a framework and its use is for ethical hacking and computer security
keywords:
  - labsecurity
  - security
  - lab
  - documentation
---

[![Build Status](https://img.shields.io/github/stars/dylan14567/labsecurity.svg)](https://github.com/dylan14567/labsecurity)
[![License](https://img.shields.io/github/license/dylan14567/labsecurity.svg)](https://github.com/dylan14567/labsecurity/blob/main/LICENSE)
[![dylan14567](https://img.shields.io/badge/author-dylan14567-green.svg)](https://github.com/dylan14567)
[![bug_report](https://img.shields.io/badge/bug-report-red.svg)](https://github.com/dylan14567/labsecurity/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
[![security_policy](https://img.shields.io/badge/security-policy-cyan.svg)](https://github.com/dylan14567/labsecurity/blob/main/.github/SECURITY.md)
[![Python](https://img.shields.io/badge/language-Python%20-yellow.svg)](https://www.python.org)
![logo](https://raw.githubusercontent.com/dylan14567/labsecurity/main/.github/icon.jpg)

labsecurity is a framework and its use is for ethical hacking and computer security.

By using and downloading labsecurity you are accepting its [terms and conditions](https://dylan14567.github.io/labsecurity/about#terms-and-conditions-of-use), but you also accept the [legal agreements](about)

# Introduction

- [How to use the console](#how-to-use-the-console)
  - [How the set command works](#how-the-set-command-works)
  - [Select ip](#select-ip)
  - [Select port](#select-port)
  - [How the use command works](#how-the-use-command-works)

Information about the installation and more details in: [https://github.com/dylan14567/labsecurity](https://github.com/dylan14567/labsecurity)

This page is the labsecurity project documentation

# How to use the console 

When using the labsecurity command we can use the ``` help ``` command to know the function of each command but in this guide we will give you a detail of how it works.

## How the set command works

The ``` set ``` command selects something for example with the ``` set ``` command we can specify the type of argument for example ``` set ip ``` that specifies to the console that we will select an object of type ip.

## Select ip

Inside the console when we use the ``` set ``` command, the ``` set ``` command is used to select something for example an ip and for that we would have to place for example ``` set target ```, ``` set ``` is to select but in the front it says ip because it specifies what type of argument we will use and once we do that we will have to put ``` set target 192.168.1.103 ```, in this example we will have selected an ip.

## Select port

Now that we know how the ``` set ``` command works, we just have to put, for example, ``` set port 80 ``` and that's it.

## How the use command works

The ``` use ``` command is used to use something specific, for example if we put the ``` help ``` command in the console we will get ``` use scanports ```, what it does is that you will be using ``` scanports ``` and ``` scanports ``` is used to scan several ports, but first we would have to have used ``` set ip ``` to select our ip then at the end we put ``` run ``` or ``` exploit ``` to make it work
