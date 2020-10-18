#!/usr/bin/env python

import ctags
import re
import simplejson
from ctags import CTags, TagEntry


def gen_syscalls(sct_file, x32=False):
    """
        Generate an Array of syscalls

        sct_file: File handle of the name table
        x32: the name table is 32 bit syscalls?
    """

    tags = CTags('tags')
    entry = TagEntry()
    sys_calls = []
    i = 0

    for line in sct_file:
        if line.startswith("#"):
            continue
        parts = line.split()
        if(len(parts) > 3 and parts[0] >= '0'):
            name = parts[3].encode("utf-8")
            if tags.find(entry, name, ctags.TAG_FULLMATCH | ctags.TAG_OBSERVECASE):
                found_sym = False
                while(not found_sym):
                    if(entry["kind"].decode("utf-8") == "prototype"):
                        found_sym = True
                        details = {"number": {"int": i, "hex": ("%0#4x" % (i))}, "name": name,
                                   "parameters": entry[b"signature"]}
                        if(entry[b"signature"] != "(void)"):
                            sig = entry[b"signature"].decode(
                                "utf-8").strip('()').split(',')
                        else:
                            sig = []
                        regs = {}

                        details["parameters_details"] = []
                        if(len(sig) < 6 if x32 else 7):
                            for param in sig:
                                par = param.strip()
                                par_def = None

                                if(param.find("struct") != -1):
                                    type_match = re.search(
                                        "struct (\w+)", param)
                                    if(type_match):
                                        par_entry = TagEntry()
                                        if(tags.find(par_entry, type_match.group(1).encode("utf-8"), ctags.TAG_FULLMATCH | ctags.TAG_OBSERVECASE)):
                                            if(par_entry[b'kind'] == "struct"):
                                                par_def = {'file': par_entry['file'], 'line': int(
                                                    par_entry['lineNumber'])}
                                details["parameters_details"].append(
                                    {'type': par, 'def': par_def})
                        else:
                            details["parameters_details"].append("param addr*")
                        remaining = (9 if x32 else 10) - len(details)
                        for x in range(0, remaining):
                            details["parameters_details"].append("")

                        pattern = "SYSCALL_DEFINE%d(%s" % (
                            len(sig), name.decode("utf-8").replace("sys_", ""))
                        search = "SYSCALL_DEFINE%d" % (len(sig))
                        if tags.find(entry, search.encode("utf-8"), ctags.TAG_FULLMATCH | ctags.TAG_OBSERVECASE):
                            found = False
                            while(not found):
                                if(entry["pattern"].decode("utf-8").find(pattern) == 2):
                                    # details['found'] = entry['pattern']
                                    details["definition"] = {
                                        "file": entry["file"], "lineno": int(entry['lineNumber'])}
                                    found = True
                                    break
                                if(not tags.findNext(entry)):
                                    details["definition"] = {
                                        "file": "not found", "lineno": "not found"}
                                    break
                        else:
                            details["definition"] = {
                                "file": "not found", "lineno": "not found"}
                        sys_calls.append(details)
                    else:
                        if(not tags.findNext(entry)):
                            sys_calls.append([i].append(
                                [""] * (10 if x32 else 11)))
                            break
            i += 1
        else:
            sys_calls.append(
                [i, "not implemented", "", "%0#4x" % (i)].append(
                    [""]*(7 if x32 else 8)
                )
            )
            i += 1

    return sys_calls


def main():
    # file generated by ctags --fields=afmikKlnsStz --c-kinds=+pc -R
    with open("syscall_64.tbl", "r") as file_64, open("syscall_32.tbl", "r") as file_32:

        syscalls_32 = gen_syscalls(file_32, True)
        syscalls_64 = gen_syscalls(file_64)

        print(simplejson.dumps(
            {"x86": syscalls_32, "x86_64": syscalls_64}, indent="   "))

    file_32.close()
    file_64.close()


if __name__ == "__main__":
    main()
