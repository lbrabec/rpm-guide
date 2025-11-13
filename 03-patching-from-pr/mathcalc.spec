Name:           mathcalc
Version:        0.1
Release:        1%{?dist}
Summary:        A simple command-line calculator

License:        MIT
URL:            https://github.com/lbrabec/rpm-guide-mathcalc
Source0:        %{url}/archive/v%{version}/rpm-guide-mathcalc-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
A simple command-line calculator for basic arithmetic operations
including addition, subtraction, multiplication, and division.

%prep
%autosetup -p1 -n rpm-guide-mathcalc-%{version}

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

%files
%{_bindir}/mathcalc
%doc README.md

%changelog
* Thu Nov 13 2025 Your Name <your@email.com> - 0.1-1
- Initial package

