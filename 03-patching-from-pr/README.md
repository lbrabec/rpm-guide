# 03 - Patching from Pull Requests

## Goal

Fix a broken build by applying a patch from an upstream PR.

## Scenario

In this example, we have package [mathcalc](https://github.com/lbrabec/rpm-guide-mathcalc), a simple calculator. Version 0.1 has a compilation error. Upstream software has a bug that's fixed in a PR but not yet released. You need to apply the patch to build on Fedora.

## Files

- `mathcalc.spec` - Spec file (already provided)

## Try It - Broken Build

First, let's try building the package as-is to see the failure:

```bash
# Download the source tarball (spectool reads the SourceX URLs from spec)
spectool -g mathcalc.spec

# Build SRPM
createsrpm mathcalc.spec

# Try to build
mock -r fedora-43-$(uname -m) mathcalc-0.1-1.fc43.src.rpm
```

**Expected result:** Build fails with compilation error:
```
error: implicit declaration of function 'strcmp' [-Wimplicit-function-declaration]
```

The compiler helpfully suggests: `include '<string.h>' or provide a declaration of 'strcmp'`

Check the full error in `/var/lib/mock/fedora-43-$(uname -m)/result/build.log`

## Investigate the Issue

When you encounter a build failure, it's good practice to:
1. **Check the error message** - The compiler tells us exactly what's wrong: missing `strcmp` declaration
2. **Look at the upstream repository** - look for `Url` in the spec file, in this case visit https://github.com/lbrabec/rpm-guide-mathcalc and check:
   - Are there recent commits that might fix this?
   - Are there open/closed pull requests addressing this issue?
   - Check the Issues tab for similar problems
3. **Understand the problem** - The code uses `strcmp()` but doesn't include `<string.h>`

In this case, if you browse the upstream repo, you'll find there's already a pull request that fixes this exact issue!

## Getting Patches from GitHub

Once you've identified that a fix exists in an upstream PR, GitHub makes it easy to download patches. Every pull request has a `.patch` URL:

```
https://github.com/USER/REPO/pull/PR_NUMBER.patch
```

This generates a unified diff patch that you can apply to your package.

## Fix It - Apply the Patch

**Step 1:** Download the patch from the GitHub PR:

```bash
wget https://github.com/USER/REPO/pull/PR_NUMBER.patch -O fix-missing-include.patch
```

**Step 2:** Edit `mathcalc.spec` and add the patch after Source0:

```spec
Source0:        %{url}/archive/v%{version}/rpm-guide-mathcalc-%{version}.tar.gz
Patch0:         fix-missing-include.patch
```

**Step 3:** The `%autosetup` macro automatically applies patches. It's already in the spec with `-p1` flag, that means strip the first directory level from patch paths).

### Rebuild:

```bash
# Build SRPM with patch
createsrpm mathcalc.spec

# Build RPM - this will succeed!
mock -r fedora-43-$(uname -m) mathcalc-0.1-1.fc43.src.rpm

# Install and test
sudo dnf install /var/lib/mock/fedora-43-$(uname -m)/result/mathcalc-0.1-*.rpm
mathcalc add 5 3

# Clean up
sudo dnf remove mathcalc
```

## Tips

- **Always check upstream first** - Many build issues are already fixed in git
- **Name patches descriptively** - `fix-missing-include.patch` is better than `1.patch`
- **Document in spec** - Add comments explaining what each patch does:
  ```spec
  # Fix missing string.h include - https://github.com/lbrabec/rpm-guide-mathcalc/pull/1
  Patch0:         fix-missing-include.patch
  ```
- **Use `%autosetup -p1` macro** - Strips first directory level from patch paths (almost always needed)
- **Track upstream** - Keep an eye on when fixes are released so you can drop patches

## Key Takeaway

When packaging software, build failures are common. Before creating your own fix:
- Check if upstream has already fixed it
- Look for **pull requests** or recent **commits**
- Apply patches from upstream rather than maintaining custom fixes
- Patches let you ship fixed packages without waiting for upstream releases

