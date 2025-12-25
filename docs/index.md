# Welcome to ROS2 Interface Documentation

This is an example documentation site using the `mkdocs-rosidl` plugin.

## About

The `mkdocs-rosidl` plugin automatically generates documentation for ROS2 Messages, Services, and Actions from your ROS2 workspace.

## Getting Started

1. Configure the plugin in your `mkdocs.yml`:

```yaml
plugins:
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
```

2. Build your documentation:

```bash
mkdocs build
```

3. The plugin will automatically generate interface documentation in the configured output directory.

## Features

- **Automatic Generation**: Interface documentation is generated automatically from your ROS2 workspace
- **Multiple Interface Types**: Supports Messages, Services, and Actions
- **Cross-referencing**: Links between related interfaces are automatically created
- **Markdown Output**: Generated documentation uses Markdown for easy integration

## Interface Documentation

The interface documentation can be found in the `interfaces/` directory. Each package has its own subdirectory with an index page listing all available interfaces.

For example:
- Messages: `interfaces/<package_name>/<MessageName>.md`
- Services: `interfaces/<package_name>/<ServiceName>.md`
- Actions: `interfaces/<package_name>/<ActionName>.md`
