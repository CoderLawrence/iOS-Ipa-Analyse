# coding: utf8
# author: Lawrence
# mail: coderlawrence@163.com

import sys
import os


# 解析 link map 文件，并且保存到map
def link_map_file_parser(link_map_file_tmp):
    reach_files = 0
    reach_sections = 0
    reach_symbols = 0
    size_map = {}
    while 1:
        line = link_map_file_tmp.readline()
        if not line:
            break
        if line.startswith("#"):
            if line.startswith("# Object files:"):
                reach_files = 1
                pass
            if line.startswith("# Sections:"):
                reach_sections = 1
                pass
            if line.startswith("# Symbols:"):
                reach_symbols = 1
                pass
            pass
        else:
            if reach_files == 1 and reach_sections == 0 and reach_symbols == 0:
                index = line.find("]")
                if index != -1:
                    symbol = {"file": line[index + 2: -1]}
                    key = int(line[1: index])
                    size_map[key] = symbol
                pass
            elif reach_files == 1 and reach_sections == 1 and reach_symbols == 0:
                pass
            elif reach_files == 1 and reach_sections == 1 and reach_symbols == 1:
                symbol_array = line.split("\t")
                if len(symbol_array) == 3:
                    file_key_and_name = symbol_array[2]
                    size = int(symbol_array[1], 16)
                    index = file_key_and_name.find("]")
                    if index != -1:
                        key = file_key_and_name[1:index]
                        key = int(key)
                        symbol = size_map[key]
                        if symbol:
                            if "size" in symbol:
                                symbol["size"] += size
                            else:
                                symbol["size"] = size
                            pass
                        pass
                    pass
                pass
            else:
                print "invalid #3"
                pass
    return size_map


# 输出 link map 解析到目标路径下
def write_link_map_to_result_file(size_map, link_mpa_file_path, link_map_result_file_path, analyse_group):
    total_size = 0
    a_file_map = {}
    for key in size_map:
        symbol = size_map[key]
        if "size" in symbol:
            # 是否需要分组统计，如果不需要会把.a or framework库里面的类大小输出
            if not analyse_group:
                total_size += symbol["size"]
                o_file_name = symbol["file"].split("/")[-1]
                if o_file_name in a_file_map:
                    a_file_map[o_file_name] += symbol["size"]
                    pass
                else:
                    a_file_map[o_file_name] = symbol["size"]
                    pass
                pass
            else:
                total_size += symbol["size"]
                o_file_name = symbol["file"].split("/")[-1]
                a_file_name = o_file_name.split("(")[0]
                if a_file_name in a_file_map:
                    a_file_map[a_file_name] += symbol["size"]
                    pass
                else:
                    a_file_map[a_file_name] = symbol["size"]
                    pass
                pass
        else:
            print "WARN : some error occurred for key",
            print key
    # 根据map对文件进行排序
    a_file_sorted_list = sorted(a_file_map.items(), key=lambda x: x[1], reverse=True)
    print "%s" % "=".ljust(80, '=')
    print "%s" % (link_mpa_file_path + "各模块体积汇总").center(87)
    print "%s" % "=".ljust(80, '=')
    if os.path.exists(link_map_result_file_path):
        os.remove(link_map_result_file_path)
        pass
    print "Creating Result File : %s" % link_map_result_file_path
    output_file = open(link_map_result_file_path, "w")
    for item in a_file_sorted_list:
        # 判断文件大小
        if item[1] / 1024.0 / 1024.0 > 1:
            print "%s%.2fM" % (item[0].ljust(80), item[1] / 1024.0 / 1024.0)
            output_file.write("%s \t\t\t%.2fM\n" % (item[0].ljust(55), item[1] / 1024.0 / 1024.0))
            pass
        else:
            print "%s%.2fK" % (item[0].ljust(55), item[1] / 1024.0)
            output_file.write("%s \t\t\t%.2fK\n" % (item[0].ljust(55), item[1] / 1024.0))
            pass
        pass
    print "%s%.2fM" % ("总体积:".ljust(53), total_size / 1024.0 / 1024.0)
    print "\n\n\n\n\n"
    output_file.write("%s%.2fM" % ("总体积:".ljust(53), total_size / 1024.0 / 1024.0))
    output_file.close()


# 检查linkMap是否合法
def check_link_map_content(link_map_content):
    obj_file_tag_index = link_map_content.find("# Object files:")
    sub_obj_file_symbol_str = link_map_content[obj_file_tag_index + 15:]
    symbols_index = sub_obj_file_symbol_str.find("# Symbols:")
    if obj_file_tag_index == -1 or symbols_index == -1 or link_map_content.find("# Path:") == -1:
        return False
    return True


# 解析link map 文件并且输出到指定目录下
def red_link_map_file(base_link_map_file_path, link_map_result_file_path):
    try:
        link_map_file = open(base_link_map_file_path)
    except IOError:
        print "read link map file" + base_link_map_file_path + "failed!"
        return
    else:
        try:
            content = link_map_file.read()
        except IOError:
            print "read link map file" + base_link_map_file_path + "failed!"
        else:
            # 检查link map 的合法性
            if not check_link_map_content(content):
                print "the content of file" + base_link_map_file_path + "is invalid"
                pass
            link_map_file_tmp = open(base_link_map_file_path)
            size_map = link_map_file_parser(link_map_file_tmp)
            if not size_map:
                print "the link map parser" + base_link_map_file_path + "failed!"
                pass
            # analyse_group 参数需要传入，目前是写死的
            write_link_map_to_result_file(size_map, base_link_map_file_path, link_map_result_file_path, False)
            link_map_file_tmp.close()
        finally:
            link_map_file.close()


def parse_result_file(result_file_path):
    base_bundle_list = []
    result_file = open(result_file_path)
    # 逐行读取文件
    while 1:
        line = result_file.readline()
        if not line:
            break
        bundle_and_size = line.split()
        if len(bundle_and_size) == 2 and line.find(":") == -1:
            bundle_and_size_map = {"name:": bundle_and_size[0], "size": bundle_and_size[1]}
            base_bundle_list += [bundle_and_size_map]
            pass
    return base_bundle_list


# 比较两个 link map的差异
def compare_link_map(base_bundle_list, target_bundle_list):
    print "%s" % "=".ljust(80, '=')
    print "%s" % "比较结果".center(84)
    print "%s" % "=".ljust(80, '=')
    print "%s%s%s%s" % ("模块名称".ljust(54), "基线大小".ljust(14), "目标大小".ljust(14), "是否新模块".ljust(14))
    for target_bundle_map in target_bundle_list:
        target_name = target_bundle_map["name"]
        target_size = target_bundle_map["size"]
        # 需要考虑单位不一致问题
        target_size_value = float(target_size.split("M")[0])
        if not target_size_value:
            target_size_value = float(target_size.split("K")[0])
            pass
        else:
            # 处理单位对齐问题
            if target_size_value > 0:
                target_size_value *= 1024
                pass
            # pass
        has_bundle_in_base = 0
        base_size_value = 0
        for base_bundle_map in base_bundle_list:
            base_name = base_bundle_map["name"]
            if base_name == target_name:
                base_size = base_bundle_map["size"]
                base_size_value = float(base_size.split("M")[0])
                if not base_size_value:
                    base_size_value = float(base_size_value.split("K")[0])
                    pass
                else:
                    # 处理单位对齐问题
                    if base_size_value > 0:
                        base_size_value *= 1024
                        pass
                    pass
                has_bundle_in_base = 1
                if base_size_value < target_size_value:
                    print "%s%s%s" % (target_name.ljust(50), str("%.2fK" % base_size_value).ljust(10),
                                      str("%.2fK" % target_size_value).ljust(10))
                    pass
                break
            pass
        if has_bundle_in_base == 0:
            print "%s%s%s%s" % (target_name.ljust(50), str("%.2fK" % base_size_value).ljust(10),
                                str("%.2fK" % target_size_value).ljust(10), "Y".center(10))
            pass
        pass


def print_help():
    print "%s" % "=".ljust(80, '=')
    print "%s%s\n" % ("".ljust(10), "Link Map 文件分析工具".ljust(80))
    print "%s%s\n" % ("".ljust(10), "- Usage : python ios_ipa_analyse.py arg1 <arg2>".ljust(80))
    print "%s%s" % ("".ljust(10), "- arg1 ：基准LinkMap文件路径".ljust(80))
    print "%s%s\n" % ("".ljust(10), "- arg2 ：待比较LinkMap文件路径".ljust(80))
    print "%s%s" % ("".ljust(10), "备注：参数2为空时，只输出基准LinkMap分析结果".ljust(80))
    print "%s" % "=".ljust(80, '=')


def clean_result_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        pass


def ios_ipa_analyse():
    if len(sys.argv) == 2:
        need_compare = 0
        pass
    elif len(sys.argv) == 3:
        need_compare = 1
        pass
    else:
        print_help()
        return
        pass

    base_map_link_file = sys.argv[1]
    output_file_path = os.path.dirname(base_map_link_file)
    if output_file_path:
        base_output_file = output_file_path + "/link_map_result.txt"
        pass
    else:
        base_output_file = "link_map_result.txt"
        pass
    red_link_map_file(base_map_link_file, base_output_file)

    if need_compare == 1:
        target_map_link_file = sys.argv[2]
        output_file_path = os.path.dirname(target_map_link_file)
        if output_file_path:
            target_output_file = output_file_path + "/target_link_map_result.txt"
            pass
        else:
            target_output_file = "target_link_map_result.txt"
            pass
        red_link_map_file(target_map_link_file, target_output_file)

        base_bundle_list = parse_result_file(base_output_file)
        target_bundle_list = parse_result_file(target_output_file)

        compare_link_map(base_bundle_list, target_bundle_list)

    # clean_result_file(base_output_file)
    # clean_result_file(target_output_file)


if __name__ == '__main__':
    ios_ipa_analyse()
