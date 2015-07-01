# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input


# Tokens
tokens = [ 'OTAG', 'CTAG' , 'CLASS', 'CONTENT']
t_ignore = "\t"
t_OTAG = r'<([a-z]+(\s?))'
t_CTAG = r'<\/([a-z]+)>'
t_CLASS = r'class\=\"([a-z]+)\"'
t_CONTENT = r'(\s?[a-zA-Z0-9])+'



literals = ['>']

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = ()

# dictionary of names
objects = []

def p_obj(p):
    '''
    obj : OTAG ">" CTAG
        | OTAG ">" CONTENT CTAG
        | OTAG ">" obj CTAG
        | OTAG CLASS ">" CTAG
        | OTAG CLASS ">" CONTENT CTAG
        | OTAG CLASS ">" obj CTAG
    '''
    objects.append(p)
    if len(p) == 4 and p[1].split("<")[1].replace(" ","") == p[3].split("/")[1].split(">")[0]: 

        print  'otag',p[1]+">",'ctag',p[3]

    elif len(p) == 5 and p[1].split("<")[1].replace(" ","") == p[4].split("/")[1].split(">")[0]: 

        if p[2] == ">":

            print  'otag',p[1].replace(" ","")+">",'class',None,'content',p[3],'ctag',p[4]

        else:

            print  'otag',p[1].replace(" ","")+">",'class',p[2],'content',None,'ctag',p[4]

    elif len(p) > 5 and p[1].split("<")[1] == p[5].split("/")[1].split(">")[0]: 

        print  'otag',p[1].replace(" ","")+">",'class', p[2],'content',p[4],'ctag',p[5]


# def p_object(p):
#     'object : OTAG CONTENT CTAG'
#     print 'object: name',p[1],'content', p[2], 'ctag', p[3]


# def p_statement_assign(p):
#     'statement : NAME "=" expression'
#     names[p[1]] = p[3]

# def p_statement_expr(p):
#     'statement : expression'
#     print(p[1])

# def p_expression_binop(p):
#     '''expression : expression '+' expression
#                   | expression '-' expression
#                   | expression '*' expression
#                   | expression '/' expression'''
#     if p[2] == '+'  : p[0] = p[1] + p[3]
#     elif p[2] == '-': p[0] = p[1] - p[3]
#     elif p[2] == '*': p[0] = p[1] * p[3]
#     elif p[2] == '/': p[0] = p[1] / p[3]

# def p_expression_binop(p):
#     '''expression : expression '+' expression
#                   | expression '-' expression
#                   | expression '*' expression
#                   | expression '/' expression'''
#     if p[2] == '+'  : p[0] = p[1] + p[3]
#     elif p[2] == '-': p[0] = p[1] - p[3]
#     elif p[2] == '*': p[0] = p[1] * p[3]
#     elif p[2] == '/': p[0] = p[1] / p[3]

# def p_expression_uminus(p):
#     "expression : '-' expression %prec UMINUS"
#     p[0] = -p[2]

# def p_expression_group(p):
#     "expression : '(' expression ')'"
#     p[0] = p[2]

# def p_expression_number(p):
#     "expression : NUMBER"
#     p[0] = p[1]

# def p_expression_name(p):
#     "expression : NAME"
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print("Undefined name '%s'" % p[1])
#         p[0] = 0

# def p_error(p):
#     if p:
#         print("Syntax error at '%s'" % p.value)
#     else:
#         print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('hola: ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)