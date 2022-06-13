
    .data                                   # STARTS DATA SEGMENT (VARIABLES)
    dt_Object:   
    dt_IO:   
    dt_Int:   
    dt_String:   
    dt_Bool:   
    dt_Main:   
    dt_Z:   
    dt_A:   
    dt_B:   
    dt_C:   
    dt_D:   
    dt_Test:   
    dt_Object:    ['abort', 'type_name', 'copy']:
    dt_IO:    ['out_string', 'out_int', 'in_string', 'in_int']:
    dt_Int:    []:
    dt_String:    ['length', 'concat', 'substr']:
    dt_Bool:    []:
    dt_Main:    ['main']:
    dt_Z:    []:
    dt_A:    []:
    dt_B:    []:
    dt_C:    []:
    dt_D:    []:
    dt_Test:    ['f', 'g', 'h']:
            .globl heap_start
                heap_start
                .word 0
        