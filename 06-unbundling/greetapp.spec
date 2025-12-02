Name:           greetapp
Version:        0.1
Release:        1%{?dist}
Summary:        CLI greeting application

License:        MIT
URL:            https://github.com/lbrabec/rpm-guide-greetapp
Source0:        %{url}/archive/v%{version}/rpm-guide-greetapp-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc

%description
A simple CLI application that greets users.

%prep
%autosetup -n rpm-guide-greetapp-%{version}

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license README.md
%{_bindir}/greetapp

%changelog
* Mon Dec 02 2024 Your Name <your@email.com> - 0.1-1
- Initial package
