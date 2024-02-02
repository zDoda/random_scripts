#!/bin/zsh

# Define paths and filenames
TEST_DIR="./tests"
REPORT_DIR="./reports"
REPORT_FILE="test_report_$(date +%F_%T).txt"

# Create the reports directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Clean previous reports
echo "Cleaning previous report files..."
rm -f "$REPORT_DIR"/*.txt

# Run tests and generate report
for TEST_SCRIPT in $TEST_DIR/*.sh; do
    if [ -f "$TEST_SCRIPT" ]; then
        TEST_NAME=$(basename "$TEST_SCRIPT")
        echo "Running test: $TEST_NAME"
        
        # Run the test script and capture its output and exit status
        TEST_OUTPUT=$("$TEST_SCRIPT" 2>&1)
        TEST_STATUS=$?
        
        # Write the results to the report file
        {
            echo "Test: $TEST_NAME"
            echo "--------------------------"
            echo "$TEST_OUTPUT"
            if [ $TEST_STATUS -eq 0 ]; then
                echo "Result: PASS"
            else
                echo "Result: FAIL"
            fi
            echo "--------------------------"
            echo ""
        } >> "$REPORT_DIR/$REPORT_FILE"
        
    else
        echo "Warning: Skipping $TEST_SCRIPT (not a valid file)"
    fi
done

echo "All tests completed. Report generated at $REPORT_DIR/$REPORT_FILE."
