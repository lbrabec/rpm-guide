# 04 - Creating Custom Patches

## Goal

Learn to create your own patches using git.

## Scenario

Sometimes the RPM builds, but resulting binary doesn't work properly. This time there is no upstream pull-request and you'll need to create a custom patch to fix it.

## Files

- `uppercase.spec` - Spec file (already provided)

## Try It

First, build and test the package to see the segfault:

```bash
# Download the source tarball
spectool -g uppercase.spec

# Build SRPM
createsrpm uppercase.spec

# Build RPM
mock -r fedora-43-$(uname -m) uppercase-1.0-1.fc43.src.rpm

# Install
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/uppercase-1.0-*.rpm

# Run the app 
uppercase "hello world"
```

**Expected result:** The package builds successfully but segfaults when run:
```
Segmentation fault (core dumped)
```

I won't keep you in suspense, the bug is that the code tries to write somewhere where it shouldn't. It this case `uppercase` pointer is initialized to `NULL` and passed to `to_uppercase()`, which tries to write to it. We'll need `malloc()` to allocate the memory.

Clean up before creating the fix:
```bash
sudo dnf remove uppercase
```

## Fix It - Create Custom Patch

You already downloaded the source tarball using `spectool -g`, now extract it and initialize git repo:

```bash
tar xf rpm-guide-uppercase-0.1.tar.gz
cd rpm-guide-uppercase-0.1

git init
git add .
git commit -m "Initial commit"
```
### Fix the bug: allocate memory for uppercase buffer
Open `main.c` in editor and change initialization of `uppercase` to:

```C
char *uppercase = malloc(strlen(argv[1]) + 1);
```
### Create the patch
```bash
git commit -am "Fix segfault by allocating memory for output buffer"
git format-patch -1 --stdout > ../fix-segfault.patch
```

## In Your Spec

Add the patch after `Source0`:

```spec
Source0:        %{url}/archive/v%{version}/rpm-guide-uppercase-%{version}.tar.gz
Patch0:         fix-segfault.patch
```

The `%autosetup` macro already in the spec will automatically apply it.

## Rebuild with the patch

Now rebuild the package with the patch applied:

```bash
# Build SRPM with patch
createsrpm uppercase.spec

# Build RPM
mock -r fedora-43-$(uname -m) uppercase-0.1-1.fc43.src.rpm

# Install and test - should work now!
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/uppercase-0.1-*.rpm
uppercase "hello world"
```

**Expected result:**
```
HELLO WORLD
```

Success! The patch fixed the segfault.

```bash
# Clean up
sudo dnf remove uppercase
```

## Alternative: Manual Diff

If you prefer not to use git:

```bash
cp -r rpm-guide-uppercase-0.1 rpm-guide-uppercase-0.1.orig
# make changes in rpm-guide-uppercase-0.1/
diff -Naur rpm-guide-uppercase-0.1.orig rpm-guide-uppercase-0.1 > fix.patch
```

## Best Practices

- One logical change per patch
- Descriptive commit messages become patch headers
- Test the patch applies cleanly: `patch -p1 < fix.patch`
- Submit patches upstream when possible

## Debugging Patch Application

```bash
# Test if patch applies cleanly
cd rpm-guide-uppercase-0.1
patch -p1 --dry-run < ../fix-segfault.patch
```

## Key Takeaway

git format-patch creates maintainable, submittable patches easily.

