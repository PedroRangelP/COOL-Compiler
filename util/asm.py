from string import Template

tpl_start_text = """
    .text                                   # STARTS TEXT SEGMENT (CODE)"""

tpl_start_data = """
    .data                                   # STARTS DATA SEGMENT (VARIABLES)"""

tpl_attribute = Template("""
$varname:   .word $value                    # Variable declaration""")

tpl_attribute_string = Template("""
$varname:   .asciiz $value                  # String declaration""")

tpl_assignment = Template("""
$prev
    sw      $$a0        $name               # Save value""")

tpl_dispatch_table = Template("""
    dt_${name}:    $methods:"""
)

tpl_name_table = Template("""
    dt_${name}:   """
)

tpl_prot_obj = Template("""
${klass_name}_protObj:
    .word   $klass_tag
    .word   $object_size
    .word   $dispatch_pointer""")

tpl_prot_obj_attribute = Template("""
    .word   $attribute""")

tpl_end = """
    li	    $v0     10                      # 10 para terminar la emulación
    syscall"""

tpl_immediate = Template("""
    li      $$a0    $immediate              # Load immediate value""")

tpl_sum = Template("""
$left
    sw      $$a0    0($$sp)                 # sum: save in the stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)                 # sum: retrieve partial previous result
    addiu   $$sp    $$sp        4           # sum: pop
    add     $$a0    $$a0        $$t1        # sum: operate""")

tpl_substract = Template("""
$left
    sw      $$a0    0($$sp)                 # substract: save in the stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)                 # substract: retrieve partial previous result
    addiu   $$sp    $$sp        4           # substract: pop
    sub     $$a0    $$t1        $$a0        # substract: operate""")

tpl_less_than = Template("""
$left
    sw      $$a0    0($$sp)                 # substract: save in the stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)                 # substract: retrieve partial previous result
    addiu   $$sp    $$sp        4           # substract: pop
    blt     $$t1    $$a0        lt$n        # substract: branch if lt
    li      $$a0    0
    j       label_exit_lt$n
lt$n:
    li      $$a0    1
label_exit_lt$n:
""")

tpl_print_int = Template("""
$prev
	li	    $$v0     1                      # Print integers
	syscall			                        # Print""")

tpl_print_str = Template("""
$prev
	li	    $$v0     4                      # Print String
	syscall			                        # Print""")

tpl_var = Template("""
    lw      $$a0        $name               # Use variable""")

tpl_var_from_stack = Template("""
    lw      $$a0        $offset($$fp)       # Reference to $name
""")

tpl_assign_from_stack = Template("""
$prev
    sw      $$a0        $offset($$fp)       # Reference to $name
""")

tpl_string_const = Template("""
    la      $$a0        $name               # Load variable address""")

tpl_if = Template("""
$prev
    beqz    $$a0        label$n             # if: predicate is 0?
$stmt_true
label$n:                                    # if: exit""")

tpl_if_else = Template("""
$prev
    beqz    $$a0        label$n             # if-else: predicate is 0?
$stmt_true
    j       labelexit$n                     # if-else: go to exit
label$n:                                    # if-else: else case
$stmt_false
labelexit$n:                                # if-else: exit label""")

tpl_while = Template("""
label_test$n:                               # while: start label
$test
    beqz    $$a0   label_exit$n             # while: predicate is 0?
$stmt
    j       label_test$n                    # while: return to the start
label_exit$n:                               # while: end while label""")

tpl_procedure = Template("""
$name:
    addiu   $$sp    $$sp        -$frame_size  # function $name: recalculate stack
    sw      $$ra    8($$sp)                  # function $name: prolog, save ra
    sw      $$fp    4($$sp)                  # function $name: prolog, save fp
    addiu   $$fp    $$sp        $frame_size
     
$code
    lw      $$fp    4($$sp)                 # function $name: postlog, restore fp
    lw      $$ra    8($$sp)                 # function $name: postlog, restore ra
    addiu   $$sp    $$sp        $stack_size # pop fp, ra, locals, params
    jr      $$ra                            # function $name: return to caller""")

tpl_push_arg = """
    sw      $a0    0($sp)                   # call: save param in the stack
    addiu   $sp    $sp          -4"""

tpl_call = Template("""
$push_arguments
    jal     $name                           # transfer control!""")
