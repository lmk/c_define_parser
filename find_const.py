#/usr/bin/python
'''c const(define, enum) parser.
value to const.
input value 0x00000 hexadecimal, 0000000 decimal.
'''

import re

FILE_PATH=['a_error.h', \
'b_Error.h', \
'c_ERROR.h']

context = ''
for fn in FILE_PATH:
    f = open(fn)
    context = context + '\n' + f.read()
    f.close()

# 1. parsing enum
dic_command = {}

def remove_comment(s):
    s = re.sub('\/\/.*[\r\n]', '', s)  # remove line comment
    s = re.sub('\/\*.*\*\/', '', s)    # remove part comment
    return s.strip()

regx = re.compile('\s*enum[_\w\s]*{([^\}]*)\}')
for enum_group in regx.findall(context):
    enum_value = 0
    for enum_item in enum_group.split(','):
        enum_item = remove_comment(enum_item)
        v_pos = enum_item.find('=')
        if v_pos == -1:
           enum_key = enum_item.strip()
           enum_value = enum_value + 1
        else:
           enum_key = enum_item[:v_pos-1].strip()
           enum_value = eval(enum_item[v_pos+1:])
        if enum_key:
            dic_command[enum_key] = str(enum_value)

# 2. parsing '#define name value'
regx = re.compile('^[ \t]*\#define[ \t]+([\w_]+)[ \t]+([^\n\r\f\v//]+)', re.MULTILINE)
define_pair = regx.findall(context)
for k, v in define_pair:
    dic_command[k] = str(v)

# 3. chage defined name to value
def change_name_to_value(v):
    if type(v) is int:
        return v
    regx = re.compile('[\w_]+')
    list_candi = regx.findall(v)
    if len(list_candi) > 1:
        for candi in list_candi:
            changed_value = change_name_to_value(candi)
            v = v.replace(candi, str(changed_value))
        return eval(v)
    if not v in dic_command:
        return eval(v)
    return change_name_to_value(dic_command[v])

for k, v in dic_command.iteritems():
    dic_command[k] = change_name_to_value(v)

dic_command_r = {}
for k, v in dic_command.iteritems():
    dic_command_r[v] = k

import sys

for argv in sys.argv[1:]:
    try:
        k = eval(argv)
    except:
        print 'convert ' + argv + ' to int fail.'
        continue

    if not k in dic_command_r:
        print argv + ' is not found.'
    else:
        print argv + ' is ' + str(dic_command_r[k])
