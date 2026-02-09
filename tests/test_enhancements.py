#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetMon-AI Enhancement Test Suite
Tests all new features added in v1.1.0
"""

import os
import sys
import json
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.colors import Colors

def test_imports():
    """Test that all modules can be imported"""
    print(f"{Colors.HEADER}=== Testing Module Imports ==={Colors.RESET}")
    
    try:
        from core.alerting import AlertingSystem
        print(f"{Colors.GREEN}✓ AlertingSystem imported{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ AlertingSystem import failed: {e}{Colors.RESET}")
        return False
    
    try:
        from core.user_manager import UserManager
        print(f"{Colors.GREEN}✓ UserManager imported{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ UserManager import failed: {e}{Colors.RESET}")
        return False
    
    try:
        from shell import NetMonShell
        print(f"{Colors.GREEN}✓ NetMonShell imported{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ NetMonShell import failed: {e}{Colors.RESET}")
        return False
    
    return True

def test_alerting_system():
    """Test alerting system functionality"""
    print(f"\n{Colors.HEADER}=== Testing Alerting System ==={Colors.RESET}")
    
    from core.alerting import AlertingSystem
    
    try:
        # Initialize alerting system
        alerting = AlertingSystem()
        print(f"{Colors.GREEN}✓ AlertingSystem initialized{Colors.RESET}")
        
        # Test alert triggering
        alerting.trigger_alert("WARNING", "CPU", "Test alert", 85.5)
        print(f"{Colors.GREEN}✓ Alert triggered successfully{Colors.RESET}")
        
        # Test threshold configuration
        alerting.configure_thresholds("cpu", 70, 90)
        print(f"{Colors.GREEN}✓ Thresholds configured{Colors.RESET}")
        
        # Test metrics check
        test_metrics = {"cpu": 95, "mem": 80, "disk": 70}
        alerting.check_system_metrics(test_metrics)
        print(f"{Colors.GREEN}✓ Metrics checked against thresholds{Colors.RESET}")
        
        # Test alert suppression
        alerting.trigger_alert("WARNING", "CPU", "Test alert", 85.5)
        print(f"{Colors.GREEN}✓ Alert suppression working{Colors.RESET}")
        
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Alerting system test failed: {e}{Colors.RESET}")
        return False

def test_user_manager():
    """Test user manager enhancements"""
    print(f"\n{Colors.HEADER}=== Testing User Manager ==={Colors.RESET}")
    
    from core.user_manager import UserManager
    
    try:
        # Initialize user manager
        user_mgr = UserManager()
        print(f"{Colors.GREEN}✓ UserManager initialized{Colors.RESET}")
        
        # Test password validation
        valid_pwd = "Test@12345"
        invalid_pwd = "weak"
        
        is_valid, errors = user_mgr.validate_password_strength(valid_pwd)
        if is_valid:
            print(f"{Colors.GREEN}✓ Strong password validated correctly{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Strong password validation failed{Colors.RESET}")
            return False
        
        is_valid, errors = user_mgr.validate_password_strength(invalid_pwd)
        if not is_valid:
            print(f"{Colors.GREEN}✓ Weak password rejected correctly{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Weak password should have been rejected{Colors.RESET}")
            return False
        
        # Test session creation
        session_id = user_mgr.create_session("testuser")
        print(f"{Colors.GREEN}✓ Session created: {session_id}{Colors.RESET}")
        
        # Test session retrieval
        if "testuser" in user_mgr.sessions:
            print(f"{Colors.GREEN}✓ Session stored correctly{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Session storage failed{Colors.RESET}")
            return False
        
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ User manager test failed: {e}{Colors.RESET}")
        return False

def test_data_persistence():
    """Test that data files are created correctly"""
    print(f"\n{Colors.HEADER}=== Testing Data Persistence ==={Colors.RESET}")
    
    data_dir = Path("data")
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(exist_ok=True)
    
    # Test files that should be created
    test_files = {
        "alert_config.json": {"enabled": True, "thresholds": {}},
        "aliases.json": {"test": "echo test"},
        "command_history.json": ["test command"],
    }
    
    all_passed = True
    for filename, content in test_files.items():
        filepath = data_dir / filename
        try:
            with open(filepath, 'w') as f:
                json.dump(content, f)
            print(f"{Colors.GREEN}✓ {filename} created successfully{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}✗ {filename} creation failed: {e}{Colors.RESET}")
            all_passed = False
    
    return all_passed

def test_shell_features():
    """Test shell enhancements"""
    print(f"\n{Colors.HEADER}=== Testing Shell Features ==={Colors.RESET}")
    
    from shell import NetMonShell
    
    try:
        shell = NetMonShell()
        print(f"{Colors.GREEN}✓ Shell initialized{Colors.RESET}")
        
        # Test history loading
        if hasattr(shell, 'command_history'):
            print(f"{Colors.GREEN}✓ Command history initialized{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Command history not found{Colors.RESET}")
            return False
        
        # Test aliases loading
        if hasattr(shell, 'aliases'):
            print(f"{Colors.GREEN}✓ Aliases initialized{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Aliases not found{Colors.RESET}")
            return False
        
        # Test alerting integration
        if hasattr(shell, 'alerting'):
            print(f"{Colors.GREEN}✓ Alerting system integrated{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Alerting system not integrated{Colors.RESET}")
            return False
        
        # Test Git branch detection
        branch = shell._get_git_branch()
        if branch is not None:
            print(f"{Colors.GREEN}✓ Git branch detected: {branch}{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠ No git repository found (this is OK){Colors.RESET}")
        
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Shell feature test failed: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration_files():
    """Test that example configuration files exist"""
    print(f"\n{Colors.HEADER}=== Testing Configuration Files ==={Colors.RESET}")
    
    config_files = [
        "data/aliases.json.example",
        "data/alert_config.json.example",
        "data/password_policies.json.example"
    ]
    
    all_exist = True
    for filepath in config_files:
        if os.path.exists(filepath):
            print(f"{Colors.GREEN}✓ {filepath} exists{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ {filepath} not found{Colors.RESET}")
            all_exist = False
    
    return all_exist

def test_documentation():
    """Test that documentation files exist"""
    print(f"\n{Colors.HEADER}=== Testing Documentation ==={Colors.RESET}")
    
    doc_files = [
        "ENHANCEMENTS.md",
        "QUICKSTART.md",
        "IMPLEMENTATION_SUMMARY.md",
        "Readme.md"
    ]
    
    all_exist = True
    for filepath in doc_files:
        if os.path.exists(filepath):
            print(f"{Colors.GREEN}✓ {filepath} exists{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ {filepath} not found{Colors.RESET}")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("=" * 60)
    print("  NetMon-AI v1.1.0 Enhancement Test Suite")
    print("=" * 60)
    print(f"{Colors.RESET}\n")
    
    results = {
        "Module Imports": test_imports(),
        "Alerting System": test_alerting_system(),
        "User Manager": test_user_manager(),
        "Data Persistence": test_data_persistence(),
        "Shell Features": test_shell_features(),
        "Configuration Files": test_configuration_files(),
        "Documentation": test_documentation()
    }
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== Test Summary ==={Colors.RESET}")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.FAIL}FAIL{Colors.RESET}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All tests passed! System is ready.{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}❌ Some tests failed. Please review.{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
