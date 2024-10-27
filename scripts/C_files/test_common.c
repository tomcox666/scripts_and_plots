// test_common.c
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <stdint.h>
#include <cmocka.h>
#include "common.h"

// Mocked functions for file operations
bool seek_and_read_bytes(uint8_t *destination, size_t destination_length, size_t position, FILE *f);
bool seek_and_write_bytes(uint8_t *source, size_t source_length, size_t position, FILE *f);

// Mock implementations for seek_and_read_bytes
bool __wrap_seek_and_read_bytes(uint8_t *destination, size_t destination_length, size_t position, FILE *f) {
    check_expected(destination_length);
    check_expected(position);
    memcpy(destination, mock_ptr_type(uint8_t *), destination_length);
    return mock_type(bool);
}

// Mock implementations for seek_and_write_bytes
bool __wrap_seek_and_write_bytes(uint8_t *source, size_t source_length, size_t position, FILE *f) {
    check_expected(source_length);
    check_expected(position);
    return mock_type(bool);
}

// Test for size_t_to_long()
static void test_size_t_to_long(void **state) {
    (void) state; // Avoid unused parameter warning
    long out;
    
    // Test for normal case
    assert_true(size_t_to_long(10, &out));
    assert_int_equal(out, 10);
    
    // Test for edge case: size_t value is larger than LONG_MAX
    // Assuming size_t is larger than long on this platform
    assert_false(size_t_to_long(SIZE_MAX, &out));
}

// Test for string_to_uintmax()
static void test_string_to_uintmax(void **state) {
    (void) state; // Avoid unused parameter warning
    uintmax_t out;
    
    // Valid number conversion
    assert_true(string_to_uintmax("12345", 10, &out));
    assert_int_equal(out, 12345);
    
    // Edge case: non-numeric input
    assert_false(string_to_uintmax("notanumber", 10, &out));
}

// Test for same_pattern()
static void test_same_pattern(void **state) {
    (void) state; // Avoid unused parameter warning
    struct ignorable_byte pattern[] = {
        { .value = 0x01, .is_ignored = false },
        { .value = 0x02, .is_ignored = true },
        { .value = 0x03, .is_ignored = false },
    };
    uint8_t bytes[] = {0x01, 0xFF, 0x03};
    assert_true(same_pattern(pattern, sizeof(pattern)/sizeof(pattern[0]), bytes, sizeof(bytes)/sizeof(bytes[0])));
    
    // Edge case: no match
    uint8_t bytes_no_match[] = {0x01, 0xFF, 0x04};
    assert_false(same_pattern(pattern, sizeof(pattern)/sizeof(pattern[0]), bytes_no_match, sizeof(bytes_no_match)/sizeof(bytes_no_match[0])));
}

// Test for seek_and_read_bytes()
static void test_seek_and_read_bytes(void **state) {
    (void) state; // Avoid unused parameter warning
    uint8_t buffer[10] = {0};
    uint8_t mock_data[10] = {1,2,3,4,5,6,7,8,9,10};
    
    // Normal case
    expect_value(__wrap_seek_and_read_bytes, destination_length, 10);
    expect_value(__wrap_seek_and_read_bytes, position, 0x140000000);
    will_return(__wrap_seek_and_read_bytes, mock_data);
    will_return(__wrap_seek_and_read_bytes, true);
    assert_true(seek_and_read_bytes(buffer, 10, 0x140000000, NULL));
    assert_memory_equal(buffer, mock_data, 10);
    
    // Edge case: fread failure
    expect_value(__wrap_seek_and_read_bytes, destination_length, 10);
    expect_value(__wrap_seek_and_read_bytes, position, 0x140000000);
    will_return(__wrap_seek_and_read_bytes, mock_data);
    will_return(__wrap_seek_and_read_bytes, false);
    assert_false(seek_and_read_bytes(buffer, 10, 0x140000000, NULL));
}

// Test for seek_and_write_bytes()
static void test_seek_and_write_bytes(void **state) {
    (void) state; // Avoid unused parameter warning
    uint8_t buffer[10] = {1,2,3,4,5,6,7,8,9,10};

    // Normal case
    expect_value(__wrap_seek_and_write_bytes, source_length, 10);
    expect_value(__wrap_seek_and_write_bytes, position, 0x140000000);
    will_return(__wrap_seek_and_write_bytes, true);
    assert_true(seek_and_write_bytes(buffer, 10, 0x140000000, NULL));
    
    // Edge case: fwrite failure
    expect_value(__wrap_seek_and_write_bytes, source_length, 10);
    expect_value(__wrap_seek_and_write_bytes, position, 0x140000000);
    will_return(__wrap_seek_and_write_bytes, false);
    assert_false(seek_and_write_bytes(buffer, 10, 0x140000000, NULL));
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_size_t_to_long),
        cmocka_unit_test(test_string_to_uintmax),
        cmocka_unit_test(test_same_pattern),
        cmocka_unit_test(test_seek_and_read_bytes),
        cmocka_unit_test(test_seek_and_write_bytes),
    };

    return cmocka_run_group_tests(tests, NULL, NULL);
}