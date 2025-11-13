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

## Basic Terminology

- **Spec file** - Recipe for building an RPM
- **BuildRequires** - Packages needed to build
- **Requires** - Packages needed to run
- **%prep** - Unpacks sources and applies patches
- **%build** - Compiles the software
- **%install** - Installs to buildroot
- **%files** - Lists files to include in RPM
- **Mock** - Clean room build environment
- **SRPM** - Source RPM (spec + sources)

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

