# Usage Guide for mkdocs-rosidl

This guide provides detailed instructions on how to use the mkdocs-rosidl plugin.

## Prerequisites

Before using the plugin, ensure you have:

1. **ROS2 installed** - The plugin requires a ROS2 environment
2. **Python 3.8+** installed
3. **MkDocs installed** - `pip install mkdocs`
4. **ROS2 Python packages**:
   ```bash
   # These are typically included with ROS2
   pip install rosidl-runtime-py rosidl-parser ament-index-python
   ```

## Installation

Install the plugin using pip:

```bash
pip install mkdocs-rosidl
```

Or for development:

```bash
git clone https://github.com/f0reachARR/mkdocs-rosidl.git
cd mkdocs-rosidl
pip install -e .
```

## Basic Configuration

### 1. Create or Update mkdocs.yml

Add the plugin to your `mkdocs.yml` configuration file:

```yaml
site_name: My ROS2 Documentation
site_description: Documentation for my ROS2 project

plugins:
  - search
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
        - sensor_msgs
      output_dir: interfaces
```

### 2. Build Documentation

Run MkDocs to build your documentation:

```bash
mkdocs build
```

Or serve it locally for development:

```bash
mkdocs serve
```

The plugin will automatically generate interface documentation during the build process.

## Configuration Options

### packages

**Type:** `list` (default: `[]`)

List of ROS2 package names to generate documentation for. If empty, all available packages in your ROS2 workspace will be documented.

**Example:**

```yaml
plugins:
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
        - sensor_msgs
        - my_custom_msgs
```

### output_dir

**Type:** `string` (default: `"interfaces"`)

Directory (relative to `docs_dir`) where interface documentation will be generated.

**Example:**

```yaml
plugins:
  - rosidl:
      packages: []  # All packages
      output_dir: ros_interfaces
```

## Generated Documentation Structure

After building, the plugin generates documentation with the following structure:

```
docs/
└── interfaces/              # or your configured output_dir
    ├── std_msgs/
    │   ├── index.md        # Package index
    │   ├── Bool.md         # Message documentation
    │   ├── String.md
    │   └── Header.md
    ├── geometry_msgs/
    │   ├── index.md
    │   ├── Point.md
    │   ├── Pose.md
    │   └── Transform.md
    └── sensor_msgs/
        ├── index.md
        ├── Image.md
        └── LaserScan.md
```

## Using Generated Documentation

### Linking to Interfaces

You can link to generated interface documentation from your main documentation:

```markdown
# My ROS2 Node

This node subscribes to [sensor_msgs/Image](interfaces/sensor_msgs/Image.md) 
and publishes [geometry_msgs/Pose](interfaces/geometry_msgs/Pose.md).
```

### Adding to Navigation

Add the generated documentation to your MkDocs navigation:

```yaml
nav:
  - Home: index.md
  - User Guide: guide.md
  - Interfaces:
    - Overview: interfaces/index.md
    - std_msgs: interfaces/std_msgs/index.md
    - geometry_msgs: interfaces/geometry_msgs/index.md
```

## Advanced Usage

### Multiple Documentation Sites

You can create different documentation builds for different sets of packages:

**docs/mkdocs.yml** (main documentation):
```yaml
plugins:
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
      output_dir: core_interfaces
```

**docs_advanced/mkdocs.yml** (advanced documentation):
```yaml
plugins:
  - rosidl:
      packages:
        - sensor_msgs
        - nav_msgs
        - tf2_msgs
      output_dir: advanced_interfaces
```

### Custom Themes

The generated Markdown integrates well with all MkDocs themes. Example with Material theme:

```yaml
theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
    - toc.integrate

plugins:
  - search
  - rosidl:
      packages: []
      output_dir: interfaces
```

### Integration with Other Plugins

The rosidl plugin works well with other MkDocs plugins:

```yaml
plugins:
  - search
  - rosidl:
      packages:
        - std_msgs
  - autorefs          # Automatic reference resolution
  - awesome-pages     # Flexible navigation
  - minify:           # Minify HTML
      minify_html: true
```

## Troubleshooting

### Plugin Not Found

**Error:** `Plugin 'rosidl' not found`

**Solution:** Ensure the plugin is installed:
```bash
pip install mkdocs-rosidl
```

### ROS2 Packages Not Found

**Error:** `Package name ... is not defined`

**Solution:** Source your ROS2 workspace:
```bash
source /opt/ros/<distro>/setup.bash
source ~/ros2_ws/install/setup.bash
mkdocs build
```

### Empty Documentation

**Issue:** Documentation is generated but pages are empty

**Solution:** Check that the specified packages contain interfaces:
```bash
ros2 interface list | grep <package_name>
```

### Import Errors

**Error:** `No module named 'rosidl_runtime_py'`

**Solution:** Install required dependencies:
```bash
pip install rosidl-runtime-py rosidl-parser ament-index-python
```

## Examples

### Example 1: Basic Robot Documentation

```yaml
site_name: My Robot Documentation

theme:
  name: readthedocs

plugins:
  - search
  - rosidl:
      packages:
        - geometry_msgs
        - sensor_msgs
        - nav_msgs

nav:
  - Home: index.md
  - Getting Started: getting_started.md
  - ROS2 Interfaces: interfaces/
  - API Reference: api/
```

### Example 2: Complete Documentation Site

```yaml
site_name: ROS2 Project Documentation
site_url: https://example.com/docs
repo_url: https://github.com/example/my-ros2-project

theme:
  name: material
  palette:
    primary: indigo
    accent: indigo

plugins:
  - search
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
        - sensor_msgs
        - my_custom_msgs
      output_dir: interfaces

nav:
  - Home: index.md
  - Installation: installation.md
  - User Guide:
    - Overview: guide/overview.md
    - Tutorials: guide/tutorials.md
  - ROS2 Interfaces:
    - Overview: interfaces/index.md
    - Standard Messages: interfaces/std_msgs/index.md
    - Geometry: interfaces/geometry_msgs/index.md
    - Sensors: interfaces/sensor_msgs/index.md
    - Custom: interfaces/my_custom_msgs/index.md
  - API Reference: api/

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
```

## Best Practices

1. **Source ROS2 before building**: Always source your ROS2 workspace before running `mkdocs build`
2. **Use specific package lists**: List specific packages instead of documenting all to keep docs focused
3. **Organize navigation**: Create a clear navigation structure for your interface documentation
4. **Add context**: Include overview pages that explain how interfaces are used in your project
5. **Version control**: Commit generated documentation if you want to track changes over time
6. **Automate builds**: Set up CI/CD to automatically rebuild documentation when interfaces change

## Further Reading

- [MkDocs Documentation](https://www.mkdocs.org/)
- [ROS2 Interface Documentation](https://docs.ros.org/en/rolling/Concepts/About-ROS-Interfaces.html)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
