#!/bin/zsh

# Constants
TEST_DIR="./tests"
REPORT_DIR="./reports"
REPORT_FILE="${REPORT_DIR}/report_$(date +%Y%m%d_%H%M%S).txt"

# Create report directory if it doesn't exist
mkdir -p "${REPORT_DIR}"

# Start testing
{
    echo "Test Report for $(date)"
    echo "============================="
    echo ""

    # Find all the test scripts in the test directory and execute them
    for test_script in "${TEST_DIR}"/*; do
        if [[ -x "${test_script}" ]]; then
            echo "Running $(basename "${test_script}")..."
            if output=$("${test_script}" 2>&1); then
                echo "PASSED: $(basename "${test_script}")"
                echo "---------"
                echo "${output}"
            else
                echo "FAILED: $(basename "${test_script}")"
                echo "---------"
                echo "${output}"
            fi
            echo ""
        fi
    done
    
    echo "============================="
    echo "End of Test Report"
} | tee "${REPORT_FILE}"

# End of script
