import upc_check_digit


def edi_convert(edi_process, output_filename, calc_upc, inc_arec, inc_crec, inc_headers, filter_ampersand):

    # save input parameters as variables
    conv_calc_upc = calc_upc
    conv_inc_arec = inc_arec
    conv_inc_crec = inc_crec
    conv_inc_headers = inc_headers
    work_file = open(edi_process)  # open input file
    work_file_lined = [n for n in work_file.readlines()]  # make list of lines
    f = open(output_filename, 'w')  # open work file, overwriting old file

    if conv_inc_headers != 0:  # include headers if flag is set
        f.write("{}" "," "{}" "," "{}" "," "{}" "," "{}" "," "{}" "," "{}\n".format("UPC", "Qty. Shipped", "Cost",
                "Suggested Retail", "Description", "Case Pack", "Item Number"))  # write line out to file

    for line_num, line in enumerate(work_file_lined):  # iterate over work file contents

        if line.startswith("A") and conv_inc_arec != 0:  # if include "A" records flag is set and line starts with "A"
            f.write(line)  # write "A" line

        # the following block writes "B" lines, dependent on filter and convert settings
        # ternary conditional operator: puts if-then-else statement in one line
        # syntax: <expression1> if <condition> else <expression2>
        # needs to be wrapped an parenthesis to separate statements

        if line.startswith("B"):
            f.write("{}\t" "," "{}\t" "," "{}\t" "," "{}\t" "," "{}" "," "{}\t" "," "{}\t" ",\n".format
                    ((upc_check_digit.add_check_digit(line[1:12]) if conv_calc_upc != 0 else line[1:12]),
                     line[60:62], line[45:47] + "." + line[47:49], line[63:65] + "." + line[65:67],
                     (line.replace("&", "AND")[12:37] if filter_ampersand != 0 else line[12:37]),
                     line[55:57], line[38:43]))

        if line.startswith("C") and conv_inc_crec != 0:  # if include "C" records flag is set and line starts with "C"
            f.write(line)  # write "C" line

    f.close()  # close output file
