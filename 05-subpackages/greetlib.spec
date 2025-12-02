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

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Headers and development files for %{name}.

%package examples
Summary: examples for %{name}
Requires: %{name}%{?_isa}

%description examples
executable example for greetlib

%package doc
Summary: docs for greetlib
BuildArch: noarch

%description doc
docs for greetlib

%prep
%autosetup -n rpm-guide-greetlib-%{version}

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license README.md
%{_libdir}/libgreet.so.0*

%files devel
%{_includedir}/greetlib.h
%{_libdir}/libgreet.so

%files examples
%{_libexecdir}/greetlib/

%files doc
%doc %{_docdir}/greetlib/

%changelog
* Mon Dec 02 2024 Your Name <your@email.com> - 0.1-1
- Initial package
