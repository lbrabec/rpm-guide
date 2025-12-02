# 00 - Getting Started

## Installation

On Fedora:
```bash
sudo dnf install fedora-packager fedora-review
sudo dnf install mock rpm-build rpmdevtools
```

Add yourself to the mock group:
```bash
sudo usermod -a -G mock $USER
newgrp mock
```

## Basic Terminology

### Package Types
- **RPM** - Binary package containing files (binaries, scripts, libraries, etc.) and metadata
- **SRPM** - Source RPM containing spec file, source tarballs, and patches

### Key Files
- **Spec file** - Recipe describing how to build an RPM package

### Dependencies
- **BuildRequires** - Packages needed during build time (compilers, headers, build tools)
- **Requires** - Packages needed at runtime (libraries, interpreters)

### Spec File Sections (Common Ones)
- **%prep** - Unpacks sources and applies patches
- **%build** - Compiles the software
- **%install** - Installs files to buildroot (staging directory)
- **%files** - Lists which files to include in the final RPM

**Note:** This is not an exhaustive list. See the [RPM Packaging Guide](https://rpm-packaging-guide.github.io/) for complete documentation.

### Build Environment
- **Mock** - Isolated chroot environment for reproducible clean-room builds
- **buildroot** - Temporary staging directory where files are installed before packaging

## RPM Packaging Tools

- **rpmbuild** - Builds RPMs and SRPMs from spec files
  - `rpmbuild -bs mypackage.spec` - build source RPM
  - `rpmbuild -bb mypackage.spec` - build binary RPM
- **mock** - Builds packages in isolated chroot environments
  - `mock -r fedora-43-x86_64 mypackage.src.rpm` - build RPM in clean environment
  - `mock --shell -r fedora-43-x86_64` - open shell in mock environment for debugging
- **rpm** - Query and manage installed RPM packages
  - `rpm -qR package-name` - show package runtime dependencies
  - `rpm -ql package-name` - list files in installed package
  - `rpm -qf /usr/bin/gcc` - find which package owns a file
- **spectool** - Downloads source files listed in spec files
  - `spectool -g mypackage.spec` - download all sources from URLs in spec
- **fedpkg** - Fedora package management tool for working with dist-git
  - `fedpkg clone package-name` - clone Fedora package repository
  - `fedpkg srpm` - build SRPM in dist-git checkout

**Note:** These are just common examples - each tool has many more options and capabilities. See man pages for complete documentation.

## Useful alias for working in project directories

Add this to your `~/.bashrc` (recommended):

```bash
alias createsrpm='rpmbuild --define "_topdir ." --define "_sourcedir ." --define "_srcrpmdir ." --define "dist .fc43" --define "_builddir ." --define "_rpmdir ." -bs'
```

This lets you build SRPMs directly in your working directory instead of ~/rpmbuild. It is basically what `fedpkg srpm` does, but that needs to be run in dist-git checkout, while this alias will work everywhere.

After adding to `~/.bashrc`, reload it:
```bash
source ~/.bashrc
```

**Note:** The dist tag `.fc43` is for Fedora 43. Adjust if using a different version (e.g., `.fc44` for Fedora 44).

## RPM File Structure

RPM files are compressed archives with metadata. They use cpio format internally, compressed with gzip, xz, or zstd.

Examine RPM contents:
```bash
# List files in RPM
rpm -qlp mypackage-1.0-1.fc43.x86_64.rpm

# Extract all files from RPM
rpm2cpio mypackage-1.0-1.fc43.x86_64.rpm | cpio -idmv

# View RPM metadata
rpm -qip mypackage-1.0-1.fc43.x86_64.rpm
```

**Tip:** Midnight Commander (`mc`) can browse RPM files directly - just navigate to an `.rpm` file and press Enter to explore its contents.

## Quick Reference

Build SRPM and test in mock:
```bash
# In your project directory with .spec file and sources
createsrpm mypackage.spec

# Build in clean environment (this dynamically detects your architecture, so this guide can be used on all platforms, obviously you can use fedora-43-x86_64, fedora-43-aarch64, etc...)
mock -r fedora-43-$(uname -m) mypackage-1.0-1.fc43.src.rpm
```

## Next Steps

Proceed to `01-basics` to build your first RPM.

