#! /usr/bin/env python3

import argparse
from os.path import basename, splitext, isdir, abspath, join
from os import getcwd


class comments:

    def __init__(self, comment_lines):
        self.comment_lines = []
        temp_buffer = str()
        for each_line in comment_lines:
            each_line = each_line.strip('*/ \t\n')
            if each_line:
                if each_line.startswith('@'):
                    if temp_buffer:
                        self.comment_lines.append(temp_buffer)
                    temp_buffer = each_line
                else:
                    temp_buffer += ' ' + each_line
        if temp_buffer:
            self.comment_lines.append(temp_buffer)

    def get_properties(self):
        '''
        Process the comments and retrieve info from them.
        FOR NOW ONLY FUNCTIONS, METHODS OR CTORS WILL BE PARSED.
        '''
        temp = ''.join(self.comment_lines).split('@')
        comment_start = temp[1].split(' ')[0]
        if comment_start != "method" and comment_start != "function" and comment_start != "construct":
            return False
        else:
            properties = dict({
                'desc': None,
                'is_what': None,
                'access': None,
                'name': None,
                'params': [],
                'returns': [],
                'throws': []
            })
            for each_line in temp:
                if each_line:
                    line_tag = "Line -> " + each_line
                    try:
                        if each_line.startswith("method") or each_line.startswith("func") or each_line.startswith("construct"):
                            if properties['is_what'] is None:
                                is_what, name = each_line.split(' ')
                                properties['is_what'] = is_what
                                properties['name'] = name
                            else:
                                raise Exception(
                                    "Invalid comment.. @func or @method or @construct tag found again in a single comment", line_tag)
                        elif each_line.startswith("access"):
                            if properties['access'] is None:
                                parsed_access = each_line.split(' ')
                                if len(parsed_access) == 2:
                                    properties['access'] = parsed_access[1]
                                else:
                                    raise Exception(
                                        "Invalid comment.. access val not specified with @access tag", line_tag)
                            else:
                                raise Exception(
                                    "Invalid comment.. @access tag found again in a single comment", line_tag)
                        elif each_line.startswith("desc"):
                            if properties['desc'] is None:
                                firstSpacePos = each_line.find(' ')
                                desc = each_line[firstSpacePos + 1:]
                                properties['desc'] = desc
                            else:
                                raise Exception(
                                    "Invalid comment.. @desc tag found again in a single comment", line_tag)
                        elif each_line.startswith("param"):
                            openParenPos = each_line.find('{')
                            closeParenPos = each_line.find('}')
                            if openParenPos < 0 or closeParenPos < 0:
                                raise Exception(
                                    "Invalid comment.. @param '{' or '}' missing", line_tag)
                            else:
                                parsed_param = []
                                type_name = each_line[openParenPos +
                                                      1:closeParenPos]
                                parsed_param.append(type_name)
                                name_and_desc = each_line[closeParenPos +
                                                          2:].split(' ', 1)
                                if len(name_and_desc) != 2:
                                    raise Exception(
                                        "Invalid comment.. @param tag takes 3 values", line_tag)
                                else:
                                    parsed_param.extend(name_and_desc)
                                    parsed_param[0], parsed_param[1] = parsed_param[1], parsed_param[0]
                                    properties['params'].append(
                                        parsed_param)
                        elif each_line.startswith("returns"):
                            openParenPos = each_line.find('{')
                            closeParenPos = each_line.find('}')
                            if openParenPos < 0 or closeParenPos < 0:
                                raise Exception(
                                    "Invalid comment.. @returns '{' or '}' missing", line_tag)
                            else:
                                parsed_ret = []
                                type_name = each_line[openParenPos +
                                                      1:closeParenPos]
                                parsed_ret.append(type_name)
                                desc = each_line[closeParenPos + 2:]
                                parsed_ret.append(desc)
                                properties['returns'].append(parsed_ret)
                        else:
                            raise Exception(
                                "Invalid comment.. Line starting with unknown tag found", line_tag)
                    except Exception:
                        raise Exception(line_tag)
            return properties

    def __str__(self):
        COMMENT_TAG = "=" * 10 + "COMMENT" + "=" * 10 + '\n'
        return COMMENT_TAG + '\n'.join(self.comment_lines)


class code:

    def __init__(self, code_lines):
        self.code_lines = ''.join(code_lines)

    def get_properties(self):
        '''
        Process the code and retrieve info from them.
        FOR NOW THIS ONLY RETURNS THE PROTOTYPE OF FUNCS, METHS, CTORS.
        '''
        firstParenPos = self.code_lines.find('{')
        firstSemiColPos = self.code_lines.find(';')
        if firstParenPos > 0 and firstSemiColPos > 0:
            firstEncountered = min(firstParenPos, firstSemiColPos)
        elif firstParenPos > 0 and firstSemiColPos < 0:
            firstEncountered = firstParenPos
        elif firstParenPos < 0 and firstSemiColPos > 0:
            firstEncountered = firstSemiColPos
        else:
            raise Exception(
                "Invalid code.. No ';' or '{' encountered while extracting function prototype, ", self.code_lines)
        return self.code_lines[:firstEncountered]

    def __str__(self):
        CODE_TAG = "." * 10 + "CODE" + "." * 10 + '\n'
        return CODE_TAG + self.code_lines


class segment:

    def __new__(segment, comment_lines, code_lines):
        # This __new__ method only allows object creation if comm.getproperties
        # does not return False i.e. the segment object will only be constructed
        # if segment is of function/method/constructor.
        temp_comm = comments(comment_lines)
        res = temp_comm.get_properties()
        if res is not False:
            return object.__new__(segment)
        else:
            return None

    def __init__(self, comment_lines, code_lines):
        self.__comm = comments(comment_lines)
        self.__code = code(code_lines)
        try:
            self.prop = self.__comm.get_properties()
            self.prop['prototype'] = self.__code.get_properties()
            first_non_whitespace_pos = len(self.prop['prototype']) - len(self.prop['prototype'].lstrip())
            if self.prop['prototype'].startswith("inline", first_non_whitespace_pos):
                before_inline_part = self.prop['prototype'][:first_non_whitespace_pos]
                after_inline_part = self.prop['prototype'][first_non_whitespace_pos+len("inline"):]
                self.prop['prototype'] =  before_inline_part + after_inline_part
        except:
            raise

    def generate_md(self):

        md_string = str()
        md_string += "## **{name}**\n\n".format(**self.prop)
        
        if self.prop['desc'] is not None:
            md_string += ">{desc}\n".format(**self.prop)
        
        md_string += "```\n{prototype}\n```".format(**self.prop)

        if self.prop['params']:
            md_string += '\n### PARAMETERS:\n'
            header = '''| NAME | TYPE | DESCRIPTION |
|------ | ------ | -------------|
'''
            md_string += header

            param_str = str()
            for each_list in self.prop['params']:
                param_str += ('|' + '|'.join(each_list) + '|\n')
            md_string += param_str

        if self.prop['returns']:
            md_string += '\n### RETURN VALUE:\n'
            header = '''|TYPE | DESCRIPTION |
|------|-------------|
'''
            md_string += header
            ret_str = str()
            for each_list in self.prop['returns']:
                ret_str += ('|' + '|'.join(each_list) + '|\n')
            md_string += ret_str
            
        md_string += '\n___\n'
        return md_string

    def __str__(self):
        return self.__comm.__str__() + "\n" + self.__code.__str__()

    def __repr__(self):
        return self.__str__()


class parser():

    def __order_segments(self, segments_list):
        # segments_list is supposed to be a list of triplets of integers like this:
        # [(1, 0, 14), (3, 0, 4), (2, 0, 7), (16, 0, 17), (15, 0, 18),
        #                (10, 0,13), (5,0, 6), (8,0, 9), (11, 0,12)]
        # Each triplet denoting (comm_start, comm_end, segment_end)
        limit = max([max(e) for e in segments_list]) + 1
        segments_list.append((-1, -1, limit,))
        segments_list.sort(key=lambda ele: ele[0])

        def core_order_segments(passed_idx):
            # TODO: Fix extra appends at the end of list
            current_tuple = segments_list[passed_idx]
            next_idx = passed_idx + 1
            while next_idx < len(segments_list):
                curr_pair_ans = []
                while current_tuple[0] < segments_list[next_idx][0] and segments_list[next_idx][2] < current_tuple[2]:
                    res = core_order_segments(next_idx)
                    if res is not None:
                        next_idx, temp_answer = res
                        curr_pair_ans.append(temp_answer)
                    else:
                        curr_pair_ans.append(
                            dict({segments_list[next_idx]: []}))
                        break
                return next_idx, dict({current_tuple: (curr_pair_ans)})
            return None

        return core_order_segments(0)

    def parse(self, file_name):

        # TODO: Remove any blank line from the file
        # TODO: Parse file char by char instead of line by line
        segments_found = []
        comm_start = None
        comm_end = None
        comm_and_open_paren = []

        with open(file_name) as f:
            src = f.readlines()
            for line_num, line in enumerate(src):
                line = line.strip()
                if line.startswith("/**"):
                    comm_start = line_num
                    comm_end = None

                if line.startswith("*/"):
                    comm_end = line_num

                if not(comm_start is not None and comm_end is None):
                    if ';' in line:
                        if comm_start is not None and comm_end is not None:
                            segments_found.append(
                                (comm_start, comm_end, comm_end + 1))
                            comm_start = None
                            comm_end = None

                    if '{' in line:
                        comm_and_open_paren.append(
                            (comm_start, comm_end, line_num,))
                        comm_start = None
                        comm_end = None

                    if '}' in line:
                        possible_match = comm_and_open_paren.pop()
                        if possible_match[0] is not None and possible_match[1] is not None:
                            segments_found.append(
                                (possible_match[0], possible_match[1], line_num,))

            temp = []
            for each_segment in segments_found:
                comm = src[each_segment[0]: each_segment[1] + 1]
                code = src[each_segment[1] + 1: each_segment[2] + 1]
                obj = segment(comm, code)
                if obj is not None:
                    temp.append(obj)
            segments_found = temp
        return segments_found


if __name__ == "__main__":

    try:
        arg_parser = argparse.ArgumentParser(description="Cpp doc generator")
        arg_parser.add_argument(
            "-f", nargs='+', required=True, metavar="file_names", dest="files")
        arg_parser.add_argument(
            "-d", required=False, metavar="destination directory {Default:current directory}", dest="dest_dir", default=getcwd(), type=str)
        src_files = arg_parser.parse_args().files
        dest_dir = abspath(arg_parser.parse_args().dest_dir)

        if isdir(dest_dir):
            p = parser()
            for each_file in src_files:
                output_md_file = join(dest_dir, splitext(basename(each_file))[0] + ".md")
                segments = p.parse(each_file)
                with open(output_md_file, 'w') as each_file_output:
                    for each_segment in segments:
                        md = each_segment.generate_md()
                        each_file_output.write(md)
            print("Markdowns Generted")
        else:
            raise Exception("Given destination is not a directory")
    except:
        raise
