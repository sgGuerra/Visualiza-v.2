#!/usr/bin/env python3
"""
Comprehensive test runner for the virtual assistant project.
This script runs all available tests and provides a summary of results.
"""

import sys
import os
import subprocess
import time

def run_test_file(test_file, description):
    """Run a single test file and return the result"""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")

    try:
        start_time = time.time()
        result = subprocess.run([sys.executable, test_file],
                              capture_output=True, text=True, timeout=300)
        end_time = time.time()

        if result.returncode == 0:
            print("✓ PASSED")
            print(f"Output: {result.stdout}")
            return True, end_time - start_time
        else:
            print("✗ FAILED")
            print(f"Error: {result.stderr}")
            print(f"Output: {result.stdout}")
            return False, end_time - start_time

    except subprocess.TimeoutExpired:
        print("✗ TIMEOUT (5 minutes)")
        return False, 300
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False, 0

def main():
    """Run all tests and provide summary"""
    print("VIRTUAL ASSISTANT COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    # Get the tests directory
    tests_dir = os.path.dirname(os.path.abspath(__file__))

    # Define test files and their descriptions
    test_files = [
        (os.path.join(tests_dir, "test_app.py"), "Flask App Basic Tests"),
        (os.path.join(tests_dir, "test_api_connections.py"), "API Connections Tests"),
        (os.path.join(tests_dir, "test_transcription.py"), "Whisper Transcription Tests"),
        (os.path.join(tests_dir, "test_pc_commands.py"), "PC Command Tests"),
    ]

    results = []
    total_time = 0

    for test_file, description in test_files:
        if os.path.exists(test_file):
            success, duration = run_test_file(test_file, description)
            results.append((description, success, duration))
            total_time += duration
        else:
            print(f"\n⚠ SKIPPED: {description} (file not found: {test_file})")
            results.append((description, None, 0))

    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    passed = 0
    failed = 0
    skipped = 0

    for description, success, duration in results:
        if success is None:
            print("⚠ SKIPPED")
            skipped += 1
        elif success:
            print("✓ PASSED")
            passed += 1
        else:
            print("✗ FAILED")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"{'='*60}")

    if failed > 0:
        print("\n❌ Some tests failed. Please check the output above for details.")
        return 1
    elif skipped > 0:
        print("\n⚠ All critical tests passed, but some were skipped.")
        return 0
    else:
        print("\n✅ All tests passed successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
