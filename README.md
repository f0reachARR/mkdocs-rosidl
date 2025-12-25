# mkdocs-rosidl

[English](#english) | [日本語](#japanese)

<a name="english"></a>
## English

MkDocs plugin for automatically generating documentation for ROS2 Messages, Services, and Actions.

This plugin is inspired by [ros2_generate_interface_docs](https://github.com/ros2/ros2_generate_interface_docs) and integrates ROS2 interface documentation generation directly into MkDocs.

### Features

- Automatic generation of documentation for ROS2 interfaces (Messages, Services, Actions)
- Seamless integration with MkDocs
- Support for filtering specific packages
- Markdown-based output for easy integration with existing documentation
- Cross-references between related interfaces

### Installation

```bash
pip install mkdocs-rosidl
```

Or install from source:

```bash
git clone https://github.com/f0reachARR/mkdocs-rosidl.git
cd mkdocs-rosidl
pip install -e .
```

### Usage

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

#### Configuration Options

- `packages`: List of ROS2 packages to generate documentation for. If empty, all available packages will be documented.
- `output_dir`: Directory (relative to docs_dir) where interface documentation will be generated. Defaults to `interfaces`.

### Example

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

### Requirements

- Python >= 3.8
- MkDocs >= 1.0
- ROS2 environment with the following packages:
  - rosidl-runtime-py
  - rosidl-parser
  - ament-index-python

### License

Apache License 2.0

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

<a name="japanese"></a>
## 日本語

ROS2のメッセージ/サービス/アクション情報を自動生成するMkDocsプラグインです。

このプラグインは[ros2_generate_interface_docs](https://github.com/ros2/ros2_generate_interface_docs)を参考に、ROS2インターフェースのドキュメント生成をMkDocsに直接統合したものです。

### 機能

- ROS2インターフェース（メッセージ、サービス、アクション）のドキュメントを自動生成
- MkDocsとのシームレスな統合
- 特定のパッケージをフィルタリングする機能
- Markdownベースの出力で既存のドキュメントとの統合が容易
- 関連するインターフェース間のクロスリファレンス

### インストール

```bash
pip install mkdocs-rosidl
```

またはソースからインストール:

```bash
git clone https://github.com/f0reachARR/mkdocs-rosidl.git
cd mkdocs-rosidl
pip install -e .
```

### 使用方法

`mkdocs.yml`設定ファイルにプラグインを追加します:

```yaml
plugins:
  - rosidl:
      packages:
        - std_msgs
        - geometry_msgs
        - sensor_msgs
      output_dir: interfaces  # オプション、デフォルトは'interfaces'
```

#### 設定オプション

- `packages`: ドキュメントを生成するROS2パッケージのリスト。空の場合、すべての利用可能なパッケージがドキュメント化されます。
- `output_dir`: インターフェースドキュメントが生成されるディレクトリ（docs_dirからの相対パス）。デフォルトは`interfaces`です。

### 例

設定後、プラグインはビルドプロセス中にインターフェースドキュメントを自動生成します。生成されたドキュメントは`docs/interfaces/`ディレクトリ（または設定した出力ディレクトリ）に配置されます。

例えば、パッケージリストに`std_msgs`がある場合、プラグインは以下を生成します:

```
docs/
  interfaces/
    std_msgs/
      index.md          # パッケージインデックス
      Bool.md           # メッセージドキュメント
      Header.md
      String.md
      ...
```

その後、標準的なMarkdownリンクを使用してメインドキュメントからこれらのページを参照できます:

```markdown
詳細は[std_msgs/String](interfaces/std_msgs/String.md)を参照してください。
```

### 必要要件

- Python >= 3.8
- MkDocs >= 1.0
- 以下のパッケージを含むROS2環境:
  - rosidl-runtime-py
  - rosidl-parser
  - ament-index-python

### ライセンス

Apache License 2.0

### 貢献

貢献を歓迎します！詳細は[CONTRIBUTING.md](CONTRIBUTING.md)をご覧ください。