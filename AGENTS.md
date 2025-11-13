# RPM Packaging Guide - Agent Context

## Purpose
Hands-on RPM packaging guide for Fedora/RHEL. Assumes prior Linux knowledge. Each section teaches through working examples that users build themselves.

## Structure
- **Numbered directories (00-10)**: Sequential lessons
- **XX-todo/**: Future topics to add
- Each directory contains:
  - `README.md` - Instructions and copy-pasteable spec files
- May contain:
  - `<name>-1.0/` - Source files ready for tarball creation
- No extra files - keep it minimal

## Workflow Philosophy
1. **Modern approach only**: Use `createsrpm` alias + mock, not traditional ~/rpmbuild
2. **Learn by doing**: Users copy spec files, build, observe failures, fix problems themselves
3. **Concise**: No long explanations - expect users can search/read docs
4. **Ready to use**: Source directories are pre-structured for immediate `tar czf`

## Key Conventions
- Use `fedora-43-$(uname -m)` for mock builds (dynamically detects architecture)
- Dist tag: `.fc43`
- Alias defined in 00-start, used throughout without re-explaining
- Show full command sequences: create tarball → createsrpm → mock → test → cleanup
- For learning sections (like 02): provide broken spec, let user fix it based on instructions

## Adding New Sections
- Create `NN-topic/` directory with README.md
- Add source files in `<name>-<version>/` subdirectory
- Show complete, copy-pasteable spec files in README
- Focus on one specific problem/concept per section
- Update main README.md structure list

