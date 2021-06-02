# LinkMap解析工具：检查每个类占用大小，可以输出到text文本

## 概述

一个大型的项目，只是代码段就有可能超过100M，算上armv7和arm64架构，就会超过200M。 这时候检查到底是哪个类、哪个第三方库占用了太多空间，就显得尤为重要。

这个工具是专为用来分析项目的LinkMap文件，得出每个类或者库所占用的空间大小（代码段+数据段），方便开发者快速定位需要优化的类或静态库。

这个工具使用Python开发，可以部署到构建机平台，每次构建的时候可以输出包大小差异，方便开发者关注包的大小

## 使用说明

### 1.安装Python环境

iOS_Ipa_Analyse是一个Python脚本，运行该脚本需要开发者的机器有Python环境，不过我们iOS的构建机一般是Mac，所以可以忽略。目前我使用的Python版本是2.7

### 2.运行工具

该工具支持分析一个link map文件和比较两个link map文件，运行的命令分别为：

#### 1、分析一个 link map文件

```shell
python ios_ipa_analyse.py $map_link_file_path
```

#### 输出结果：

```shell
AppDelegate.o                                     0.01K
ViewController.o                                  0.00K
main.o                                            0.00K
libobjc.tbd                                       0.00K
linker synthesized                                0.00K
Foundation.tbd                                    0.00K
UIKit.tbd                                         0.00K
总体积: 
```


## 如何获得LinkMap文件

1.在XCode中开启编译选项Write Link Map File \n
XCode -> Project -> Build Settings -> 把Write Link Map File选项设为yes，并指定好linkMap的存储位置

2.工程编译完成后，在编译目录里找到Link Map文件（txt类型) 默认的文件地址：~/Library/Developer/Xcode/DerivedData/XXX-xxxxxxxxxxxxx/Build/Intermediates/XXX.build/Debug-iphoneos/XXX.build/ \n\

## 感谢

https://github.com/huanxsd/LinkMap

https://github.com/zgzczzw/LinkMapParser


## 联系我

如果有问题欢迎联系我 coderlawrence@163.com
