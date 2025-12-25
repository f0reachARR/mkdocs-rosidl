# mkdocs-rosidl

MkDocs plugin for automatically generating documentation for ROS2 Messages, Services, and Actions.

This plugin is inspired by [ros2_generate_interface_docs](https://github.com/ros2/ros2_generate_interface_docs) and integrates ROS2 interface documentation generation directly into MkDocs.

## Features

- Automatic generation of documentation for ROS2 interfaces (Messages, Services, Actions)
- Seamless integration with MkDocs
- Support for filtering specific packages
- Markdown-based output for easy integration with existing documentation

## Installation

```bash
pip install mkdocs-rosidl
```

Or install from source:

```bash
git clone https://github.com/f0reachARR/mkdocs-rosidl.git
cd mkdocs-rosidl
pip install -e .
```

## Usage

Add the plugin to your `mkdocs.yml` configuration:

```yaml
plugins:
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
        - sensor_msgs
      output_dir: interfaces  # Optional, defaults to 'interfaces'
```

### Configuration Options

- `packages`: List of ROS2 packages to generate documentation for. If empty, all available packages will be documented.
- `output_dir`: Directory (relative to docs_dir) where interface documentation will be generated. Defaults to `interfaces`.

## Example

After configuration, the plugin will automatically generate interface documentation during the build process. The generated documentation will be placed in the `docs/interfaces/` directory (or your configured output directory).

For example, if you have `std_msgs` in your packages list, the plugin will generate:

```
docs/
  interfaces/
    std_msgs/
      index.md          # Package index
      Bool.md           # Message documentation
      Header.md
      String.md
      ...
```

You can then reference these pages in your main documentation using standard Markdown links:

```markdown
See [std_msgs/String](interfaces/std_msgs/String.md) for more details.
```

## Requirements

- Python >= 3.8
- MkDocs >= 1.0
- ROS2 environment with the following packages:
  - rosidl-runtime-py
  - rosidl-parser
  - ament-index-python

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.