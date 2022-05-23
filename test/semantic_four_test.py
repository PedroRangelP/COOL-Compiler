import pytest

from main import compile

def test_assignment():
    try:
        compile('resources/semantic/input/assignment.cool')
    except:
        assert False

def test_basic():
    try:
        compile('resources/semantic/input/basic.cool')
    except:
        assert False

def test_basicclassestree():
    try:
        compile('resources/semantic/input/basicclassestree.cool')
    except:
        assert False

def test_cells():
    try:
        compile('resources/semantic/input/cells.cool')
    except:
        assert False

def test_classes():
    try:
        compile('resources/semantic/input/classes.cool')
    except:
        assert False

def test_compare():
    try:
        compile('resources/semantic/input/compare.cool')
    except:
        assert False

def test_comparisons():
    try:
        compile('resources/semantic/input/comparisons.cool')
    except:
        assert False

def test_cycleinmethods():
    try:
        compile('resources/semantic/input/cycleinmethods.cool')
    except:
        assert False

def test_dispatch():
    try:
        compile('resources/semantic/input/dispatch.cool')
    except:
        assert False

def test_expressionblock():
    try:
        compile('resources/semantic/input/expressionblock.cool')
    except:
        assert False

def test_forwardinherits():
    try:
        compile('resources/semantic/input/forwardinherits.cool')
    except:
        assert False

def test_hairyscary():
    try:
        compile('resources/semantic/input/hairyscary.cool')
    except:
        assert False

def test_if():
    try:
        compile('resources/semantic/input/if.cool')
    except:
        assert False

def test_inheritsObject():
    try:
        compile('resources/semantic/input/inheritsObject.cool')
    except:
        assert False

def test_initwithself():
    try:
        compile('resources/semantic/input/initwithself.cool')
    except:
        assert False

def test_io():
    try:
        compile('resources/semantic/input/io.cool')
    except:
        assert False

def test_isvoid():
    try:
        compile('resources/semantic/input/isvoid.cool')
    except:
        assert False

def test_letinit():
    try:
        compile('resources/semantic/input/letinit.cool')
    except:
        assert False

def test_letnoinit():
    try:
        compile('resources/semantic/input/letnoinit.cool')
    except:
        assert False

def test_letselftype():
    try:
        compile('resources/semantic/input/letselftype.cool')
    except:
        assert False

def test_letshadows():
    try:
        compile('resources/semantic/input/letshadows.cool')
    except:
        assert False

def test_list():
    try:
        compile('resources/semantic/input/list.cool')
    except:
        assert False

def test_methodcallsitself():
    try:
        compile('resources/semantic/input/methodcallsitself.cool')
    except:
        assert False

def test_methodnameclash():
    try:
        compile('resources/semantic/input/methodnameclash.cool')
    except:
        assert False

def test_neg():
    try:
        compile('resources/semantic/input/neg.cool')
    except:
        assert False

def test_newselftype():
    try:
        compile('resources/semantic/input/newselftype.cool')
    except:
        assert False

def test_objectdispatchabort():
    try:
        compile('resources/semantic/input/objectdispatchabort.cool')
    except:
        assert False

def test_overriderenamearg():
    try:
        compile('resources/semantic/input/overriderenamearg.cool')
    except:
        assert False

def test_overridingmethod():
    try:
        compile('resources/semantic/input/overridingmethod.cool')
    except:
        assert False

def test_overridingmethod2():
    try:
        compile('resources/semantic/input/overridingmethod2.cool')
    except:
        assert False

def test_overridingmethod3():
    try:
        compile('resources/semantic/input/overridingmethod3.cool')
    except:
        assert False

def test_scopes():
    try:
        compile('resources/semantic/input/scopes.cool')
    except:
        assert False

def test_simplearith():
    try:
        compile('resources/semantic/input/simplearith.cool')
    except:
        assert False

def test_simplecase():
    try:
        compile('resources/semantic/input/simplecase.cool')
    except:
        assert False

def test_staticdispatch():
    try:
        compile('resources/semantic/input/staticdispatch.cool')
    except:
        assert False

def test_stringtest():
    try:
        compile('resources/semantic/input/stringtest.cool')
    except:
        assert False

def test_subtypemethodreturn():
    try:
        compile('resources/semantic/input/subtypemethodreturn.cool')
    except:
        assert False

def test_trickyatdispatch():
    try:
        compile('resources/semantic/input/trickyatdispatch.cool')
    except:
        assert False