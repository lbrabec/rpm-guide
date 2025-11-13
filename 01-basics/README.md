# 01 - Basic RPM

## Goal

Build a minimal "Hello World" RPM package.

## File
- `hello-1.0/hello.sh` - A simple bash script (already provided)
- `hello.spec` - The spec file you'll create


### hello.spec (read and copy-paste this)

```spec
Name:           hello
Version:        1.0
Release:        1%{?dist}
Summary:        A simple hello world script

License:        MIT
URL:            https://example.com/hello
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
A simple hello world bash script packaged as an RPM.

%prep
%setup -q

%build
# Nothing to build for a shell script

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 hello.sh %{buildroot}%{_bindir}/hello.sh

%files
%{_bindir}/hello.sh

%changelog
* Thu Nov 13 2025 Your Name <your@email.com> - 1.0-1
- Initial package
```

## The Spec File

Key sections:
- **Preamble** - Name, Version, Release, Summary, License
- **%description** - What the package does
- **%prep** - Usually just `%setup -q`
- **%build** - Compile commands (none for shell script)
- **%install** - Copy files to %{buildroot}
- **%files** - List what goes in the RPM

## Try It

Copy-paste the `hello.spec` example above into a file named `hello.spec`.

Then run:

```bash
# Create tarball (directory structure already provided)
tar czf hello-1.0.tar.gz hello-1.0/

# Build SRPM
createsrpm hello.spec

# Build RPM with mock
mock -r fedora-43-$(uname -m) hello-1.0-1.fc43.src.rpm

# Install
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/hello-1.0-*.rpm

# Run the newly installed script
hello.sh

# Clean up
sudo dnf remove hello
```

## Common Issues

- Missing Source0 tarball
- Forgotten `%install` commands
- Missing files in `%files` section

## Key Takeaway

An RPM is just files + metadata. The spec file describes how to build and package them.

