import argparse


# class comments:
#     COMMENT_TAG = "=" * 10 + "COMMENT" + "=" * 10
#     # tags =  # collection of @returns, @params etc.

#     def __init__(self, comment_lines):
#         self.comment_lines = comment_lines

#     def process(self):
#         '''
#         Process the comments and retrieve info from them
#         '''

#         print(self.COMMENT_TAG)
#         for each_line in self.comment_lines:
#             print(each_line, end='')
#         # processed_comments = []
#         # for each_line in self.comment_lines:
#         #     each_line = each_line.strip('*/ \t\n')
#         #     if each_line:
#         #         processed_comments.append(each_line)

#         # self.comment_lines = processed_comments


# class code:
#     CODE_TAG = "." * 10 + "CODE" + "." * 10

#     def __init__(self, code_lines):
#         self.code_lines = code_lines

#     def process(self):
#         print(self.CODE_TAG)
#         for each_line in self.code_lines:
#             print(each_line, end='')

#         # return code_lines


class segment:
    def __init__(self, comment_lines, code_lines):
        self.comm = comments(comment_lines)
        self.code = code(code_lines)


class composite_segment():
    # TODO: maintain a collection of segments
    pass


def join_segments(segments_list):
    # TODO: Change this function according to list of tuples of 3 numbers
    # print("..join_segments speaking, got this segments list: ", segments_list)
    limit = max([max(e) for e in segments_list]) + 1
    segments_list.append((-1, limit,))
    segments_list.sort(key=lambda ele: ele[0])
    # print("..join_segments speaking, after sorting segments_list: ", segments_list)

    def core_join_segments(passed_idx, tabs=2):
        tabs_string = ".." * tabs + "core_join_segments speaking,"
        current_pair = segments_list[passed_idx]
        print(tabs_string, "passed_idx is: ",
              passed_idx, "current_pair: ", current_pair)
        next_idx = passed_idx + 1
        print(tabs_string, "next_idx is: ", next_idx)
        while next_idx < len(segments_list):
            curr_pair_ans = []
            while current_pair[0] < segments_list[next_idx][0] and segments_list[next_idx][1] < current_pair[1]:
                print(
                    tabs_string, "segment_list[" + str(next_idx) + "] is: ", segments_list[next_idx])
                res = core_join_segments(next_idx, tabs=tabs + 2)
                if res is not None:
                    next_idx, temp_answer = res
                    curr_pair_ans.append(temp_answer)
                else:
                    curr_pair_ans.append(dict({segments_list[next_idx]: []}))
                    break
            print(tabs_string, "about to return: ", next_idx,
                  dict({current_pair: (curr_pair_ans)}))
            return next_idx, dict({current_pair: (curr_pair_ans)})
            input()
        return None
    # def core_join_segments(passed_idx, tabs=2):

    #     tabs_string = ".." * tabs

    #     print(tabs_string + "core_join_segments speaking, passed_idx: ", passed_idx)
    #     for i in range(passed_idx, len(segments_list)):
    #         if is_calculated[i] is False:

    #             current_pair = segments_list[i]
    #             print(
    #                 tabs_string + "core_join_segments speaking, current_pair: ", current_pair)

    #             next_idx = i + 1
    #             print(tabs_string +
    #                   "core_join_segments speaking, next_idx: ", next_idx)
    #             temp_list = []

    #             while current_pair[0] < segments_list[next_idx][0] and segments_list[next_idx][1] < current_pair[1]:
    #                 print(tabs_string + "core_join_segments speaking, in while, found pair: ",
    #                       segments_list[next_idx])
    #                 print(
    #                     tabs_string + "core_join_segments speaking, isCalculated for this pair is: ", is_calculated[i])
    #                 if is_calculated[next_idx] is False:
    #                     res = core_join_segments(next_idx, tabs=tabs + 2)
    #                     # temp_dict[current_pair] = res
    #                     temp_list.append(res)
    #                 next_idx += 1
    #                 input()

    #             is_calculated[i] = True
    #             print(tabs_string +
    #                   "core_join speaking, is_calculated is: ", is_calculated)
    #             print(
    #                 tabs_string + "core_join_segments speaking, going to return this:", temp_list)
    #             # TODO: Don't return here, do something else
    #             return temp_list

    res = core_join_segments(0)
    print("..join_segments speaking: ", res)


def parse(file_path):

    # TODO: Remove any blank line from the file
    # TODO: Parse file char by char instead of line by line

    comm_start = None
    comm_end = None
    comm_and_open_paren = []
    segments = []

    with open(file_path) as f:
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
                        segments.append((comm_start, comm_end, comm_end + 1))
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
                        segments.append(
                            (possible_match[0], possible_match[1], line_num,))

    return segments


if __name__ == "__main__":

    join_segments([(1, 14), (3, 4), (2, 7), (16, 17), (15, 18),
                   (10, 13), (5, 6), (8, 9), (11, 12)])

    # arg_parser = argparse.ArgumentParser(description="Cpp doc generator")
    # arg_parser.add_argument(
    #     "-f", nargs='+', required=True, metavar="file_names", dest="files")
    # src_files = arg_parser.parse_args().files

    # for each_file in src_files:
    #     segments = parse(each_file)
    #     print("segments for file: ", each_file, "are: ")
    #     for each_segment in segments:
    #         print("segments for file: ", each_file, "are: ", each_segment)
