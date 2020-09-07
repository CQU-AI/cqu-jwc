# cqu-jxgl

[![cqu-tool-bucket](https://img.shields.io/badge/CQU-%E9%87%8D%E5%BA%86%E5%A4%A7%E5%AD%A6%E5%85%A8%E5%AE%B6%E6%A1%B6%E8%AE%A1%E5%88%92-blue)](https://github.com/topics/cqu-tool-bucket)
![Liscence](https://img.shields.io/github/license/CQU-AI/cqu-jxgl)
[![pypi](https://img.shields.io/pypi/v/cqu-jxgl)](https://pypi.org/project/cqu-jxgl/)
![download](https://pepy.tech/badge/cqu-jxgl)
![Upload Python Package](https://github.com/CQU-AI/cqu-jxgl/workflows/Upload%20Python%20Package/badge.svg)

cqu-jxgl 是一个基于python3的，重庆大学教务处登录的第三方模块。

## 特性

本模块：
1. 自动登录教务网，密码错误时抛出异常
1. 封装了带session的GET和POST请求，方便开发者使用
1. GET请求可以自动处理教务网上的DSafeId cookie机制
1. 所有HTTP请求头可以全局设置，也可以每个请求单独配置
1. 所有请求均加入了失败重试机制

## 使用

本项目是一个登录功能模块，是面向开发者而不是用户的。若需使用一些教务网相关功能，请查看[重庆大学全家桶计划](https://github.com/orgs/CQU-AI/projects/1)

## 声明
1. 本仓库Fork自[maxoyed/cqu_jwc](https://github.com/maxoyed/cqu_jwc/tree/bd09b6a433f1a50794982548c23fa014710a0a39)，为了适配[重庆大学全家桶计划](https://github.com/orgs/CQU-AI/projects/1)的其它项目，对该仓库做了一些功能性调整和重构，并加入了新的功能和特性。
1. 本程序不存储用户的帐号，密码。
