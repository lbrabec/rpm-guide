# 05 - Subpackages

## Goal

Split a library into multiple subpackages: main, -devel, -examples, -doc.

## Why Subpackages?

- Users only install what they need
- Runtime: `greetlib` (just the .so)
- Development: `greetlib-devel` (headers, unversioned .so symlink)
- Examples: `greetlib-examples` (demo binaries)
- Docs: `greetlib-doc` (documentation)

## Starting Point

Create `greetlib.spec` with this basic spec (main package only):

```spec
Name:           greetlib
Version:        0.1
Release:        1%{?dist}
Summary:        Simple greeting library

License:        MIT
URL:            https://github.com/lbrabec/rpm-guide-greetlib
Source0:        %{url}/archive/v%{version}/rpm-guide-greetlib-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc

%description
A simple greeting library for demonstration purposes.

%prep
%autosetup -n rpm-guide-greetlib-%{version}

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license README.md
%{_libdir}/libgreet.so*
%{_includedir}/greetlib.h
%{_libexecdir}/greetlib/
%{_docdir}/greetlib/

%changelog
* Mon Dec 02 2024 Your Name <your@email.com> - 0.1-1
- Initial package
```

## Try It First

Build this monolithic package:

```bash
spectool -g greetlib.spec
createsrpm greetlib.spec
mock -r fedora-43-$(uname -m) greetlib-0.1-1.fc43.src.rpm
```

Works, but everything is in one package. Let's split it.

## Task: Add the -devel Subpackage

A `-devel` subpackage needs:
- Header files
- Unversioned `.so` symlink (for linking)
- Dependency on main package

**Add this after `%description`:**

```spec
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Headers and development files for %{name}.
```

**Update `%files` section** - move header and unversioned symlink to devel:

```spec
%files
%license README.md
%{_libdir}/libgreet.so.0*
%{_includedir}/greetlib.h
%{_libexecdir}/greetlib/
%{_docdir}/greetlib/

%files devel
%{_includedir}/greetlib.h
%{_libdir}/libgreet.so
```

Notice: `libgreet.so.0*` stays in main (runtime), `libgreet.so` goes to devel (linking).

## Task: Add the -examples Subpackage

Now add `-examples` yourself. You need:
- `%package examples` section with Summary, Requires, %description
- `%files examples` section containing `%{_libexecdir}/greetlib/`

Remove `%{_libexecdir}/greetlib/` from `%files` (main package).

**Hint:** Structure is identical to -devel. The example binary links against libgreet.so, so it needs `Requires: %{name}%{?_isa}` just like -devel does.

## Task: Add the -doc Subpackage

Add `-doc` yourself. Hints:
- Docs have no compiled code, so add `BuildArch: noarch`
- Move `%{_docdir}/greetlib/` to `%files doc`
- Use `%doc` directive: `%doc %{_docdir}/greetlib/`

**Hint:** Documentation doesn't depend on the library at runtime - anyone can read docs without installing the library. So no `Requires` line needed.

## Rebuild and Verify

```bash
createsrpm greetlib.spec
mock -r fedora-43-$(uname -m) greetlib-0.1-1.fc43.src.rpm
ls /var/lib/mock/fedora-43-$(uname -m)/result/*.rpm
```

**Expected:** Four RPMs:
- `greetlib-0.1-1.fc43.x86_64.rpm`
- `greetlib-devel-0.1-1.fc43.x86_64.rpm`
- `greetlib-examples-0.1-1.fc43.x86_64.rpm`
- `greetlib-doc-0.1-1.fc43.noarch.rpm`

## Test

```bash
# Install all produced RPMs
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/greetlib*.rpm

# List files in greetlib-examples
rpm -ql greetlib-examples

# Run the example
/usr/libexec/greetlib/greet-demo

# See what libraries it links to
ldd /usr/libexec/greetlib/greet-demo

# Find which package provides libgreet.so.0
rpm -qf /usr/lib64/libgreet.so.0

# Clean up
sudo dnf remove greetlib greetlib-devel greetlib-examples greetlib-doc
```

## Reference

### Library Files Split

CMake creates versioned library and symlinks automatically via `VERSION` and `SOVERSION` properties.

| File | Package | Why |
|------|---------|-----|
| `libgreet.so.0.1.0` | greetlib | Actual library |
| `libgreet.so.0` | greetlib | SONAME symlink (runtime) |
| `libgreet.so` | greetlib-devel | Unversioned (linking only) |

### The `%{?_isa}` Macro

```spec
Requires: %{name}%{?_isa} = %{version}-%{release}
```

Ensures architecture match (e.g., 64-bit -devel requires 64-bit library).

## Key Takeaway

Use `%package` to create subpackages. Each needs its own `%description` and `%files` section.
