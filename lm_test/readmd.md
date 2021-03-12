## 安装ffmpeg
```bash
conda activate opencv
## brew就是命令简单，但是缺点是之后要等比较久，而且无法控制中途下载的包，我不知道这个FFmpeg为啥要下openjdk14，我好像有jdk..
## 在macOS下搞挺麻烦，而且容易错，所以直接上Linux服务器吧
brew install  ffmpeg
ffmpeg --version
## 安装ffmpeg的python扩展，该扩展可以让你直接在python脚本中直接调用，而不需要单独运行命令
pip install ffmpeg-python
```

`brew install ffmpeg`报错：
```
==> Downloading https://www.ijg.org/files/jpegsrc.v9d.tar.gz
Error: SHA256 mismatch
Expected: 99cb50e48a4556bc571dadd27931955ff458aae32f68c4d9c39d624693f69c32
  Actual: 6c434a3be59f8f62425b2e3c077e785c9ce30ee5874ea1c270e843f273ba71ee
 Archive: /Users/linmin/Library/Caches/Homebrew/downloads/23faa446d5ad2c8f0a288f26af4c4f70666394f107eb58154ab432da5f6705d1--jpegsrc.v9d.tar.gz
To retry an incomplete download, remove the file above.
```

报错到这里，大概花了我3个G，所以赶紧部署好Linux开发环境吧，冲