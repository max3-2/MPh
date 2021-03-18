# jpype typecast tester for arrays
import logging
import numpy as np
import jpype
import jpype.types as jtypes
import mph

logger = logging.getLogger(__name__)

# Discover Comsol back-end.
backend = mph.discovery.backend('5.5')

# Start the Java virtual machine.
jpype.startJVM(str(backend['jvm']),
               classpath=str(backend['root']/'plugins'/'*'),
               convertStrings=False)

# 0-D
test_int = 1
test_float = 1.
test_bool = True
test_string = 'valid'

# 1-D
test_int_array = np.ones((10,), dtype=int)
test_float_array = np.ones((10,), dtype=float)
test_bool_array = np.ones((10,), dtype=bool)
test_string_array = np.array([
    f'string_{i}' for i in range(10)])
test_string_object_array = test_string_array.astype(object)

# 2-D
test_int_matrix = np.ones((10, 10), dtype=int)
test_float_matrix = np.ones((10, 10), dtype=float)
test_bool_matrix = np.ones((10, 10), dtype=bool)
test_string_matrix = np.array([
    f'string_{i}' for i in range(100)]).reshape((10, 10))
test_string_object_matrix = test_string_matrix.astype(object)
# Start the tests
passed = True

# typecast 0D
try:
    _ = jtypes.JInt(test_int)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JDouble(test_float)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JBoolean(test_bool)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JString(test_string)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False

#typecast 1D
try:
    _ = jtypes.JArray(jtypes.JInt)(test_int_array)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JArray(jtypes.JDouble)(test_float_array)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JArray(jtypes.JBoolean)(test_bool_array)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    test_string_array_java = jtypes.JArray(jtypes.JString)(test_string_array)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JArray(jtypes.JString)(test_string_object_array)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False

logger.info('Testing 2D arrays')
#typecast 2D
try:
    _ = jtypes.JArray.of(test_int_matrix)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JArray.of(test_float_matrix)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    _ = jtypes.JArray.of(test_bool_matrix)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False

# JStrings work with object and numpy str dtype
try:
    test_string_matrix_java = jtypes.JString[test_string_matrix.shape]
    for i, row in enumerate(test_string_matrix):
        for j, col in enumerate(row):
            test_string_matrix_java[i][j] = col
    logger.debug(test_string_matrix_java.length)
    logger.debug(test_string_matrix_java[5].length)
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False
try:
    res = jtypes.JString[test_string_object_matrix.shape]
    for i, row in enumerate(test_string_object_matrix):
        for j, col in enumerate(row):
            res[i][j] = col
    logger.debug(res.length)
    logger.debug(res[5].length)
    logger.debug(res[5][5])
except Exception as e:
    logger.exception(f'Test failed with: {e}')
    passed = False

# Test vice versa for problematic string arrays

test_string_array_vv = np.array(
    [str(string) for string in test_string_array_java])

test_string_matrix_vv = np.array(
    [[str(string) for string in line]
     for line in test_string_matrix_java])

try:
    assert np.array_equal(test_string_array, test_string_array_vv), "ViceVersa comparison failed for str array"
    assert np.array_equal(test_string_matrix, test_string_matrix_vv), "ViceVersa comparison failed for str array"
except AssertionError:
    logger.exception()
    passed = False