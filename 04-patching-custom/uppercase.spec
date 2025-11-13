Name:           uppercase
Version:        0.1
Release:        1%{?dist}
Summary:        A simple text processing utility

License:        MIT
URL:            https://github.com/lbrabec/rpm-guide-uppercase
Source0:        %{url}/archive/v%{version}/rpm-guide-uppercase-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
A simple text processing utility that converts text to uppercase.

%prep
%autosetup -p1 -n rpm-guide-uppercase-%{version}

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

%files
%{_bindir}/uppercase
%doc README.md

%changelog
* Thu Nov 13 2025 Your Name <your@email.com> - 0.1-1
- Initial package

