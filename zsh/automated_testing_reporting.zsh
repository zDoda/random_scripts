```zsh
#!/usr/bin/env zsh

# Automated testing and reporting script
# Usage: ./test_and_report.zsh [TEST_SCRIPT] [REPORT_FILE]

# Define test script and report file from command line arguments
TEST_SCRIPT=${1?"Error: No test script provided"}
REPORT_FILE=${2?"Error: No report file specified"}

# Check if test script file exists
if [[ ! -f "$TEST_SCRIPT" ]]; then
    echo "Error: Test script $TEST_SCRIPT does not exist" >&2
    exit 1
fi

# Run the test script and capture its output
echo "Running tests..."
TEST_OUTPUT=$("$TEST_SCRIPT" 2>&1)
TEST_EXIT_CODE=$?

# Create or overwrite the report file with test results
echo "Generating report..."
echo "---- Test Report for $TEST_SCRIPT ----" >"$REPORT_FILE"
echo "Timestamp: $(date)" >>"$REPORT_FILE"
echo "--------------------------------------" >>"$REPORT_FILE"

# Check if the tests were successful based on the exit code
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    echo "Status: SUCCESS" >>"$REPORT_FILE"
else
    echo "Status: FAILURE" >>"$REPORT_FILE"
fi

# Output test results
echo "Test Output:" >>"$REPORT_FILE"
echo "--------------------------------------" >>"$REPORT_FILE"
echo "$TEST_OUTPUT" >>"$REPORT_FILE"

# End of the report
echo "--------------------------------------" >>"$REPORT_FILE"
echo "End of report" >>"$REPORT_FILE"

# Output final status to console
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    echo "Tests completed successfully, report saved to $REPORT_FILE"
else
    echo "Tests failed, check the report at $REPORT_FILE for details"
fi

exit $TEST_EXIT_CODE
