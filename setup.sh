#!/bin/bash

# 安装python依赖
pip install -r requirements.txt --proxy=127.0.0.1:7890
# pip install -r requirements.txt

# 安装ocr依赖库
brew install leptonica
brew install tesseract

