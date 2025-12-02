# 06 - Unbundling

## Goal

Learn to unbundle vendored/bundled libraries and use system packages instead.

## Why Unbundle?

Fedora policy requires using system libraries when available:
- Security updates apply to all packages at once
- Reduces duplicate code and package size
- Ensures consistent library versions

## Scenario

[greetapp](https://github.com/lbrabec/rpm-guide-greetapp) bundles greetlib as a git submodule. The CMake has an option `USE_BUNDLED_GREETLIB` (default: ON). We need to:
1. Disable bundled library
2. Use system `greetlib` instead
3. Add proper BuildRequires/Requires

## Files

- `greetapp.spec` - Spec file (provided, needs modifications)

## Try It (Bundled) - This Will Fail

```bash
spectool -g greetapp.spec
createsrpm greetapp.spec
mock -r fedora-43-$(uname -m) greetapp-0.1-1.fc43.src.rpm
```

**Expected:** Build fails - the bundled submodule isn't included in the release tarball (git submodules are not included in GitHub's auto-generated archives).

## Task: Unbundle greetlib

**Step 1:** Add BuildRequires for system library:

```spec
BuildRequires:  greetlib-devel
```

**Step 2:** Pass CMake option to disable bundled library. Update `%cmake` line:

```spec
%cmake -DUSE_BUNDLED_GREETLIB=OFF
```

**Step 3:** Add runtime dependency:

```spec
Requires:       greetlib
```

## Rebuild

greetapp needs greetlib-devel to build. Use `--chain` to build both packages in sequence - mock makes the first package available when building the second:

```bash
mock -r fedora-43-$(uname -m) --chain \
    greetlib-0.1-1.fc43.src.rpm \
    greetapp-0.1-1.fc43.src.rpm
```

**Note:** For more complex scenarios, you can create a local repo and use `--addrepo`:

```bash
createrepo /tmp/localrepo
mock -r fedora-43-$(uname -m) --addrepo=file:///tmp/localrepo greetapp-0.1-1.fc43.src.rpm
```

## Test

Find and install the built RPMs (location varies depending on build method used):

```bash
sudo dnf install /path/to/greetlib-0.1*.rpm /path/to/greetapp*.rpm

greetapp World
ldd $(which greetapp)

sudo dnf remove greetapp greetlib
```

## Finding CMake Options

Most projects document their CMake options. Common ways to find them:

```bash
# Search all CMakeLists.txt files
grep -rn "option(" --include="CMakeLists.txt" .

# Or let CMake list all options
cmake -B build -LAH

# Common patterns
-DUSE_BUNDLED_*=OFF
-DUSE_SYSTEM_*=ON
-DENABLE_*=OFF
-DWITH_*=OFF
```

## Key Takeaway

Unbundling = disable bundled libs via build flags + add system library as BuildRequires/Requires.

