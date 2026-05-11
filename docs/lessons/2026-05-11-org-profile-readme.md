# Organization README Belongs in the Profile Repository

## Context

The bluetape4k organization profile README was created through the special
`.github` repository.

## Decision or Finding

Keep organization-facing documentation in `.github/profile/README.md` and keep
project-specific documentation in each target repository.

## Outcome

The organization profile can introduce bluetape4k libraries, workshops, and
example projects without duplicating every repository README.

## Verification

- The `.github` repository owns the organization profile surface.
- Project repositories keep their own README and module documentation.

## Future Guidance

- Use the organization README for ecosystem orientation.
- Use repo README files for build, module, and usage details.
- Do not include organization profile images in the README when the GitHub
  organization profile image is already configured separately.
