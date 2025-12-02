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

