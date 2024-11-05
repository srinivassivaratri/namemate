# 🔄 Namemate

A lightning-fast CLI tool for bulk renaming files with smart presets. Perfect for developers and content creators who need to maintain consistent file naming conventions across projects.

## 🎯 Why Namemate?

Managing consistent file naming across projects is a pain. Manually renaming files is tedious and error-prone, especially when dealing with hundreds of files. Namemate solves this by providing:

- One-command bulk renaming with smart presets
- Cross-platform support (Windows/Linux/WSL)
- Safe dry-run mode to preview changes
- Flexible file filtering
- Duplicate handling

## 🚀 Quick Start

### Install

```bash
pip install namemate
```

### Basic Usage

```bash
# Replace spaces with underscores
namemate -d "/path/to/files" -o replace_spaces

# Convert to lowercase
namemate -d "/path/to/files" -o lowercase
```

## 📖 Usage

### Available Operations

- `replace_spaces` - Replace spaces with underscores
- `lowercase` - Convert to lowercase
- `uppercase` - Convert to uppercase
- `add_prefix` - Add custom prefix
- `add_suffix` - Add custom suffix
- `change_extension` - Change file extensions
- `remove_text` - Remove specific text

### Advanced Examples

Preview changes without renaming:
```bash
namemate -d "/path/to/files" -o lowercase --dry-run
```

Filter specific files:
```bash
namemate -d "/path/to/files" -o lowercase --filter "*.txt"
```

Add prefix to all images:
```bash
namemate -d "/path/to/files" -o add_prefix --filter "*.{jpg,png,gif}"
```

## 🛠️ Contributing

### Setup Development Environment

```bash
# Clone the repo
git clone https://github.com/yourusername/namemate
cd namemate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest
```

### Submit Changes

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this in your own projects!
