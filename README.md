# Link Map Parser: Tool for Checking Class Size

## Overview

In a large project, just the code section alone can exceed 100M, and with both armv7 and arm64 architectures, it can go over 200M. At this point, it becomes crucial to determine which classes or third-party libraries are taking up too much space.

This tool is designed to analyze a project's Link Map file, determining the space each class or library occupies (code section + data section). This makes it easy for developers to quickly identify classes or static libraries that need optimization.

This tool is developed in Python and can be deployed on build machine platforms. It can output package size differences each time a build occurs, enabling developers to focus on package size.

## Instructions

### 1. Install Python Environment

iOS_Ipa_Analyse is a Python script that requires Python environment on the developer's machine to run. Since our iOS build machines are generally Macs, this requirement can be ignored. Currently, I am using Python version 2.7.

### 2. Running the Tool

This tool supports analyzing a single link map file and comparing two link map files. The commands to run are as follows:

#### 1. Analyzing a Single Link Map File

```shell
python ios_ipa_analyse.py $map_link_file_path
```
##### Output:

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
#### 2. Comparing Two Link Map Files

```shell
python ios_ipa_analyse.py $map_link_file_path $target_map_link_file_path
```

Link Map Parser analyzes two map link files, compares the sizes of various modules for changes, and lists out modules that have increased in size.

##### Output is similar to:

```shell
================================================================================
                     xxx/link_map_result.txt各模块体积汇总
================================================================================
Creating Result File : xxx/link_map_result.txt
AppDelegate.o                                     0.01M
ViewController.o                                  0.00M
main.o                                            0.00M
libobjc.tbd                                       0.00M
linker synthesized                                0.00M
Foundation.tbd                                    0.00M
UIKit.tbd                                         0.00M
总体积:                                           0.01M

================================================================================
                    xxx/target_link_map_result.txt各模块体积汇总
================================================================================
Creating Result File : xxx/target_link_map_result.txt
AppDelegate.o                                     0.64K
ViewController.o                                  0.00K
main.o                                            0.00K
libobjc.tbd                                       0.00K
linker synthesized                                0.00K
Foundation.tbd                                    0.00K
UIKit.tbd                                         0.00K
总体积:                                           0.64M


================================================================================
                                    比较结果
================================================================================
模块名称                                          基线大小  目标大小  是否新模块
AppDelegate.o                                     0.01M     0.64M
```
## Obtaining the Link Map File

1、Enable the "Write Link Map File" compilation option in Xcode:

XCode -> Project -> Build Settings -> Set "Write Link Map File" to yes and specify the linkMap storage location.

2、After the project compiles, find the Link Map file (in txt format) in the build directory:

Default file location: ~/Library/Developer/Xcode/DerivedData/XXX-xxxxxxxxxxxxx/Build/Intermediates/XXX.build/Debug-iphoneos/XXX.build

## Acknowledgments

Special thanks to these developers for providing valuable references and even code snippets during my search for solutions and implementation:

 - https://github.com/huanxsd/LinkMap
 - https://github.com/zgzczzw/LinkMapParser

## Contact Me
 
 If you have any questions, feel free to reach out to me at coderlawrence@163.com.
 
## Conclusion
 
 If you find this helpful, please consider giving it a star!

