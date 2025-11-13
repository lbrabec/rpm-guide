Name:           greet
Version:        1.0
Release:        1%{?dist}
Summary:        A simple greeting program

License:        MIT
URL:            https://example.com/greet
Source0:        %{name}-%{version}.tar.gz

%description
A simple C program that prints a greeting.

%prep
%setup -q

%build
gcc $CFLAGS -o greet greet.c

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 greet %{buildroot}%{_bindir}/greet

%files
%{_bindir}/greet

%changelog
* Thu Nov 13 2025 Your Name <your@email.com> - 1.0-1
- Initial package

