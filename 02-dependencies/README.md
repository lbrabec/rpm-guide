# 02 - Dependencies

## Goal

Understand BuildRequires vs Requires and how missing deps cause build failures.

## The Problem

The spec file builds a C program but is missing `gcc` in BuildRequires.

## Files

- `greet-1.0/greet.c` - A simple C program (already provided)
- `greet.spec` - The spec file (already provided, but broken!)


## What You'll Learn

- **BuildRequires** - Needed at build time (compilers, headers, build tools)
- **Requires** - Needed at runtime (libraries, interpreters)
- **Automatic runtime dependencies** - RPM auto-detects shared library deps

## Try It

The `greet.spec` file is already provided, but it's missing a crucial dependency. Let's see what happens:

```bash
# Create tarball (directory structure already provided)
tar czf greet-1.0.tar.gz greet-1.0/

# Build SRPM
createsrpm greet.spec

# Try to build RPM with mock - this will FAIL!
mock -r fedora-43-$(uname -m) greet-1.0-1.fc43.src.rpm
```

**Expected result:** Build fails with error about missing `gcc` command.

Read the error message in `/var/lib/mock/fedora-43-$(uname -m)/result/build.log` - it will show that `gcc` is not found. 

Note: sometimes, especially with complex spec files and complex build systems, the error message itself is not at the end of `build.log` and can be **buried in other text output**. 

## Fix It

Now fix the spec file by adding the missing dependency. Open `greet.spec` in your editor and add this line after the `Source0:`:
```spec
BuildRequires:  gcc
```

### Rebuild:

```bash
# Build SRPM with fixed spec
createsrpm greet.spec

# Build RPM with mock - this will succeed!
mock -r fedora-43-$(uname -m) greet-1.0-1.fc43.src.rpm

# Install
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/greet-1.0-*.rpm

# Run the newly installed program
greet

# Clean up
sudo dnf remove greet
```

## Finding Dependencies

```bash
# What does a binary need?
ldd /path/to/binary

# What provides a file?
dnf provides /usr/bin/gcc

# What does a package require?
rpm -qR package-name
```

## Common BuildRequires

- C/C++: `gcc`, `gcc-c++`, `make`, `cmake`
- Python: `python3-devel`, `python3-setuptools`
- Autotools: `autoconf`, `automake`, `libtool`

## Key Takeaway

Build failures are often caused by missing BuildRequires. Read error messages carefully.

