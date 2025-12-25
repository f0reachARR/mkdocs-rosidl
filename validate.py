#!/usr/bin/env python3
"""
Simple validation script to check if the mkdocs-rosidl plugin can be loaded.

This script does NOT require a ROS2 environment and only validates:
- Python syntax
- Module imports
- Plugin registration
"""

import sys
from pathlib import Path

# Add the package to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import mkdocs_rosidl
        print(f"✓ mkdocs_rosidl imported successfully (version {mkdocs_rosidl.__version__})")
    except ImportError as e:
        print(f"✗ Failed to import mkdocs_rosidl: {e}")
        return False
    
    # Note: The following will fail without ROS2 dependencies, but we can at least
    # check that the syntax is correct by attempting import
    module_names = ['utils', 'msg_utils', 'srv_utils', 'action_utils', 'plugin']
    ros2_required = True
    
    for module_name in module_names:
        try:
            module = __import__(f'mkdocs_rosidl.{module_name}', fromlist=[module_name])
            print(f"✓ mkdocs_rosidl.{module_name} imported successfully")
        except ImportError as e:
            # Expected to fail without ROS2 dependencies
            if 'rosidl' in str(e).lower() or 'ament' in str(e).lower() or 'mkdocs' in str(e).lower() or 'jinja' in str(e).lower():
                print(f"⚠ mkdocs_rosidl.{module_name} requires dependencies: {e}")
                ros2_required = True
            else:
                print(f"✗ Failed to import {module_name}: {e}")
                return False
    
    return True

def test_plugin_registration():
    """Test that the plugin can be registered with MkDocs."""
    print("\nTesting plugin registration...")
    
    try:
        # This will fail if the plugin entry point is malformed
        from mkdocs_rosidl.plugin import RosidlPlugin
        print(f"✓ RosidlPlugin class found")
        
        # Check that it has the required methods
        required_methods = ['on_pre_build']
        for method in required_methods:
            if hasattr(RosidlPlugin, method):
                print(f"✓ RosidlPlugin.{method} method exists")
            else:
                print(f"✗ RosidlPlugin.{method} method not found")
                return False
        
        # Check config_scheme
        if hasattr(RosidlPlugin, 'config_scheme'):
            print(f"✓ RosidlPlugin.config_scheme exists")
        else:
            print(f"✗ RosidlPlugin.config_scheme not found")
            return False
            
    except ImportError as e:
        if any(dep in str(e).lower() for dep in ['rosidl', 'ament', 'mkdocs', 'jinja']):
            print(f"⚠ Plugin requires dependencies: {e}")
            return True  # Not a failure, just missing deps
        else:
            print(f"✗ Failed to load plugin: {e}")
            return False
    
    return True

def test_templates():
    """Test that template files exist."""
    print("\nTesting templates...")
    
    template_dir = Path(__file__).parent / 'mkdocs_rosidl' / 'templates'
    
    if not template_dir.exists():
        print(f"✗ Template directory not found: {template_dir}")
        return False
    
    print(f"✓ Template directory exists: {template_dir}")
    
    required_templates = [
        'msg.html.jinja2',
        'srv.html.jinja2',
        'action.html.jinja2',
        'index.html.jinja2',
        'styles.css',
        'msg-styles.css'
    ]
    
    for template in required_templates:
        template_path = template_dir / template
        if template_path.exists():
            print(f"✓ Template exists: {template}")
        else:
            print(f"✗ Template not found: {template}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("mkdocs-rosidl Validation Script")
    print("=" * 60)
    print()
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_plugin_registration()
    all_passed &= test_templates()
    
    print()
    print("=" * 60)
    if all_passed:
        print("✓ All validation tests passed!")
        print()
        print("Note: Full functionality testing requires a ROS2 environment with:")
        print("  - rosidl-runtime-py")
        print("  - rosidl-parser")
        print("  - ament-index-python")
    else:
        print("✗ Some validation tests failed")
        return 1
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
