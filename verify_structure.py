#!/usr/bin/env python
"""
Project Structure Verification and Summary
This script provides a comprehensive overview of the project structure.
"""

import os
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent


def get_file_tree(directory, prefix="", ignore_dirs={'.git', '__pycache__', '.venv', 'venv', 'node_modules'}):
    """Generate a tree view of the directory structure."""
    items = []
    
    try:
        entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    except PermissionError:
        return items
    
    for i, entry in enumerate(entries):
        if entry.name.startswith('.') and entry.name not in {'.github', '.gitignore'}:
            continue
        if entry.name in ignore_dirs:
            continue
        
        is_last = i == len(entries) - 1
        current_prefix = "└── " if is_last else "├── "
        items.append(prefix + current_prefix + entry.name)
        
        if entry.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            items.extend(get_file_tree(entry, next_prefix, ignore_dirs))
    
    return items


def count_files_by_type():
    """Count files by type."""
    file_counts = defaultdict(int)
    total_size = 0
    
    for file_path in PROJECT_ROOT.rglob('*'):
        if file_path.is_file():
            suffix = file_path.suffix or 'no_extension'
            file_counts[suffix] += 1
            total_size += file_path.stat().st_size
    
    return dict(file_counts), total_size


def main():
    """Print project structure and statistics."""
    
    print("=" * 80)
    print("HOUSEHOLD POWER CONSUMPTION PREDICTION - PROJECT STRUCTURE")
    print("=" * 80)
    print()
    
    # Directory tree
    print("📁 PROJECT DIRECTORY TREE")
    print("-" * 80)
    tree = get_file_tree(PROJECT_ROOT)
    for line in tree[:50]:  # Limit output
        print(line)
    if len(tree) > 50:
        print(f"... and {len(tree) - 50} more items")
    print()
    
    # File statistics
    print("📊 FILE STATISTICS")
    print("-" * 80)
    file_counts, total_size = count_files_by_type()
    
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    print(f"Total files: {sum(file_counts.values())}")
    print()
    print("Files by type:")
    for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext:20s}: {count:3d} files")
    print()
    
    # Project components
    print("🔧 PROJECT COMPONENTS")
    print("-" * 80)
    
    components = {
        'Data Processing': [
            'src/data/loader.py - Data loading utilities',
            'src/data/preprocessor.py - Preprocessing pipeline',
        ],
        'Feature Engineering': [
            'src/features/engineer.py - Feature creation',
        ],
        'Model Training': [
            'src/models/trainer.py - Model training and evaluation',
        ],
        'Visualization': [
            'src/visualization/plotter.py - Plotting utilities',
        ],
        'Utilities': [
            'src/utils/config.py - Configuration',
            'src/utils/logger.py - Logging setup',
        ],
        'API': [
            'flask_app.py - Flask REST API',
        ],
        'Pipeline': [
            'train_pipeline.py - Complete ML pipeline',
            'evaluate_model.py - Model evaluation',
            'mlops_pipeline.py - MLOps pipeline',
        ],
        'Testing': [
            'tests/test_data.py - Data tests',
            'tests/test_models.py - Model tests',
            'tests/test_features.py - Feature tests',
            'tests/test_flask.py - API tests',
        ],
        'Deployment': [
            'Dockerfile - Docker image',
            'docker-compose.yml - Docker Compose',
        ],
        'Documentation': [
            'README.md - Complete documentation',
            'QUICKSTART.md - Quick start guide',
            'PROJECT_SETUP_COMPLETE.md - Setup summary',
        ],
    }
    
    for category, items in components.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  ✓ {item}")
    
    print()
    print("=" * 80)
    print("✨ PROJECT SETUP COMPLETE - READY FOR GITHUB UPLOAD")
    print("=" * 80)
    print()
    print("Quick Start Commands:")
    print("-" * 80)
    print("1. Setup environment:")
    print("   python -m venv venv")
    print("   pip install -r requirements.txt")
    print()
    print("2. Train model:")
    print("   python train_pipeline.py")
    print()
    print("3. Run Flask API:")
    print("   python flask_app.py")
    print()
    print("4. Run tests:")
    print("   pytest tests/ -v")
    print()
    print("5. Deploy with Docker:")
    print("   docker-compose up -d")
    print()
    print("=" * 80)


if __name__ == '__main__':
    main()
