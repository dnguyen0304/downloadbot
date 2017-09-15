# Introduction
This document adheres to the specifications outlined in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

# Version Control
### Commit Messages
- Issue IDs **must** be included.
```
# YES
git commit --message "PROJECT-1: foo."

# No
git commit --message "foo."
```

# Python
### Package Hierarchy
```
       Common
       |
Scraping
```

### General
- Import statements **should** be sorted to enforce import order.
- Intra-package import statements **should** use the explicit relative form.
- Packages **should** have a `__all__` index.
- Modules **should not** have a `__all__` index.
- `__all__` indices **should** be sorted alphabetically.

### Testing
- Black-box testing **should** be favored over white-box testing.
