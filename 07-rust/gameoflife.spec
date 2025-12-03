Name:           gameoflife
Version:        0.1.0
Release:        1%{?dist}
Summary:        Conway's Game of Life TUI

License:        MIT
URL:            https://github.com/lbrabec/rpm-guide-gameoflife
Source0:        %{url}/archive/v%{version}/rpm-guide-gameoflife-%{version}.tar.gz

BuildRequires:  cargo

%description
Conway's Game of Life running in your terminal using ratatui.
Press 'q' or Esc to quit.

%prep
%autosetup -n rpm-guide-gameoflife-%{version}

%build
cargo build --release

%install
install -Dpm 755 target/release/rpm-guide-gameoflife %{buildroot}%{_bindir}/rpm-guide-gameoflife

%files
%{_bindir}/rpm-guide-gameoflife

%changelog
* Wed Dec 03 2025 Package Maintainer <maintainer@example.com> - 0.1.0-1
- Initial package
