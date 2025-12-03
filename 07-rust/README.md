# 07 - Rust Packaging

## Goal

Learn to package Rust applications using Fedora's Rust macros and system crates.

## Project

[gameoflife](https://github.com/lbrabec/rpm-guide-gameoflife) - Conway's Game of Life TUI using ratatui.

Dependencies from `Cargo.toml`:
```toml
[dependencies]
ratatui = "0.29"
crossterm = "0.28"
rand = "0.9"
```

## Try It - This Will Fail

```bash
spectool -g gameoflife.spec
createsrpm gameoflife.spec
mock -r fedora-43-$(uname -m) gameoflife-0.1.0-1.fc43.src.rpm
```

**Expected failure:** `cargo build` tries to download crates from the internet, but mock has no network access.

```
error: failed to get `crossterm` as a dependency of package `rpm-guide-gameoflife v0.1.0 (/builddir/build/BUILD/gameoflife-0.1.0-build/rpm-guide-gameoflife-0.1.0)`

Caused by:
  download of config.json failed

Caused by:
  failed to download from `https://index.crates.io/config.json`

Caused by:
  [6] Could not resolve hostname (Could not resolve host: index.crates.io)
```

## Why It Fails

The naive spec uses `cargo build` directly:

```spec
BuildRequires:  cargo

%build
cargo build --release
```

This works on your machine but fails in isolated builds (mock, koji, brew) because:
1. No network access in build environments
2. Downloads aren't reproducible
3. No security review of downloaded code

## The Solution: Fedora Rust Macros

Fedora packages thousands of Rust crates. Instead of downloading, use them as BuildRequires.

### Step 1: Use rust-packaging

Replace `cargo` with `rust-packaging`:

```spec
BuildRequires:  rust-packaging >= 21
```

### Step 2: Use %cargo macros

| Macro | Replaces |
|-------|----------|
| `%cargo_prep` | Manual .cargo/config setup |
| `%cargo_build` | `cargo build --release` |
| `%cargo_install` | Manual `install` command |
| `%cargo_test` | `cargo test` |

### Step 3: Auto-generate crate dependencies

Instead of manually listing each crate as `BuildRequires: ...`, add a `%generate_buildrequires` section. This section goes **after `%prep`** (it needs unpacked sources to read `Cargo.toml`):

```spec
%prep
%autosetup -n rpm-guide-gameoflife-%{version}
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install
```

RPM runs `%generate_buildrequires` after `%prep`, determines needed packages, installs them, then continues with `%build`.

Similar macros exist for other ecosystems:
- Python: `%pyproject_buildrequires`
- Perl: `%perl_generate_buildrequires`
- Ruby: `%gem_generate_buildrequires`

## Rebuild

```bash
createsrpm gameoflife.spec
mock -r fedora-43-$(uname -m) gameoflife-0.1.0-1.fc43.src.rpm
```

## Test

```bash
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/gameoflife-0.1.0-1.fc43.$(uname -m).rpm

rpm-guide-gameoflife  # Press 'q' to quit

sudo dnf remove gameoflife
```

## Finding Rust Crates in Fedora

When `%cargo_generate_buildrequires` fails because a crate isn't packaged, you can search:

```bash
# Search for a crate
dnf repoquery 'rust-*ratatui*'

# Check available features
dnf repoquery 'rust-ratatui+*-devel'

# See what versions exist
dnf repoquery --qf '%{name}-%{version}' 'rust-ratatui-devel'
```

## What If a Crate Isn't Packaged?

Options:
1. **Package it** - Submit to Fedora (preferred)
2. **Vendor** - Bundle dependencies (last resort, but sometimes necessary)

## Vendoring Dependencies

When crates aren't available in Fedora repos, you can bundle them.

### Step 1: Create vendor tarball

```bash
cd rpm-guide-gameoflife-0.1.0
cargo vendor
tar czf ../gameoflife-0.1.0-vendor.tar.gz vendor/
```

### Step 2: Update spec file

Add vendor tarball as source and extract it:

```spec
Source0:        %{url}/archive/v%{version}/rpm-guide-gameoflife-%{version}.tar.gz
Source1:        gameoflife-%{version}-vendor.tar.gz

%prep
%autosetup -n rpm-guide-gameoflife-%{version}
tar xf %{SOURCE1}
```

### Step 3: Configure cargo to use vendored crates

Create `.cargo/config.toml` in `%prep`:

```spec
%prep
%autosetup -n rpm-guide-gameoflife-%{version}
tar xf %{SOURCE1}
mkdir -p .cargo
cat > .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored"

[source.vendored]
directory = "vendor"
EOF
```

### Step 4: Build with cargo (no macros needed)

```spec
%build
cargo build --release --offline

%install
install -Dpm 755 target/release/rpm-guide-gameoflife %{buildroot}%{_bindir}/rpm-guide-gameoflife
```

### Step 5: Declare bundled crates

Fedora policy requires declaring bundled dependencies. List each vendored crate:

```spec
Provides:       bundled(crate(ratatui)) = 0.29.0
Provides:       bundled(crate(crossterm)) = 0.28.1
Provides:       bundled(crate(rand)) = 0.9.0
# ... and all transitive dependencies
```

Generate the list automatically:
```bash
ls vendor/ | while read crate; do
    version=$(grep '^version' "vendor/$crate/Cargo.toml" | head -1 | cut -d'"' -f2)
    echo "Provides:       bundled(crate($crate)) = $version"
done
```

### Why Vendoring Is Discouraged

- Security updates require rebuilding every package that vendors the affected crate
- Duplicates code across packages
- More work to maintain
- Review burden for Fedora packagers

Use system crates when possible; vendor only when necessary.

## Key Takeaway

`cargo build` needs network → fails in mock. Use `%cargo_*` macros + `%cargo_generate_buildrequires` to automatically use system crates.
