#!/usr/bin/env python3
"""
QXR Bridge Setup Script

Builds the Rust-C-Python bridge extension for high-performance
QXR social media integration.
"""

import os
import sys
import subprocess
from pathlib import Path
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

# Get the directory containing this setup.py
ROOT_DIR = Path(__file__).parent.absolute()
RUST_DIR = ROOT_DIR
C_BINDINGS_DIR = ROOT_DIR / "c_bindings"
PYTHON_EXT_DIR = ROOT_DIR / "python_extension"

def build_rust_library():
    """Build the Rust library with C FFI bindings"""
    print("Building Rust library...")
    
    # Change to rust directory and build
    original_cwd = os.getcwd()
    try:
        os.chdir(RUST_DIR)
        
        # Build in release mode for performance
        result = subprocess.run([
            "cargo", "build", "--release", "--lib"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Rust build failed: {result.stderr}")
            sys.exit(1)
            
        print("Rust library built successfully")
        
    finally:
        os.chdir(original_cwd)

def get_rust_library_path():
    """Get the path to the built Rust library"""
    lib_name = "libqxr_bridge"
    
    # Try different extensions
    for ext in [".so", ".dylib", ".dll"]:
        lib_path = RUST_DIR / "target" / "release" / f"{lib_name}{ext}"
        if lib_path.exists():
            return str(lib_path)
    
    # If no shared library found, try static
    for ext in [".a", ".lib"]:
        lib_path = RUST_DIR / "target" / "release" / f"{lib_name}{ext}"
        if lib_path.exists():
            return str(lib_path)
    
    raise FileNotFoundError("Could not find built Rust library")

class CustomBuildExt(build_ext):
    """Custom build extension that builds Rust first"""
    
    def run(self):
        # Build Rust library first
        build_rust_library()
        
        # Then build Python extension
        super().run()

# Define the Python extension module
def create_extension():
    """Create the Python extension configuration"""
    
    # Source files
    sources = [
        str(PYTHON_EXT_DIR / "qxr_bridge_module.c"),
        str(C_BINDINGS_DIR / "qxr_bridge_wrapper.c"),
    ]
    
    # Include directories
    include_dirs = [
        str(C_BINDINGS_DIR),
        str(RUST_DIR / "target" / "release"),
    ]
    
    # Library directories
    library_dirs = [
        str(RUST_DIR / "target" / "release"),
    ]
    
    # Libraries to link
    libraries = ["qxr_bridge"]
    
    # Runtime library directories (for shared libraries)
    runtime_library_dirs = library_dirs if sys.platform != "win32" else []
    
    # Compiler and linker flags
    extra_compile_args = []
    extra_link_args = []
    
    if sys.platform == "linux":
        extra_compile_args.extend(["-O3", "-fPIC"])
        extra_link_args.extend(["-Wl,-rpath,$ORIGIN"])
    elif sys.platform == "darwin":
        extra_compile_args.extend(["-O3"])
        extra_link_args.extend(["-Wl,-rpath,@loader_path"])
    elif sys.platform == "win32":
        extra_compile_args.extend(["/O2"])
    
    return Extension(
        name="qxr_bridge",
        sources=sources,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        runtime_library_dirs=runtime_library_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        language="c"
    )

# Read README for long description
def read_readme():
    readme_path = ROOT_DIR / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "QXR Rust-C-Python Bridge for high-performance social media integration"

# Setup configuration
setup(
    name="qxr-bridge",
    version="0.1.0",
    author="QXR Development Team",
    author_email="dev@qxr.com",
    description="High-performance Rust-C-Python bridge for QXR social media integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/calvinsthomas/OpenAIDeepSeekAIChatGPTOpenSourceCollaborationTransparency",
    packages=[],  # No pure Python packages, just extension
    ext_modules=[create_extension()],
    cmdclass={"build_ext": CustomBuildExt},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Rust",
        "Programming Language :: C",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No Python dependencies for core bridge
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-benchmark>=3.4",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-benchmark>=3.4",
            "numpy>=1.20",
        ],
    },
    zip_safe=False,  # Extension modules can't be zipped
)