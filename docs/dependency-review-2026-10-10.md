# Dependency review: October 10, 2026

## Findings and updates

Reviewed all 13 open Dependabot pull requests and the 22 open dependency alerts. The initial npm audit reported 19 affected packages, including propagated findings in parent packages. The GitHub alert count and npm package count measure different things.

| Bot PRs | Resolution on main |
| --- | --- |
| #12, #15 | Astro 7.3.8, Starlight 0.42.6, sitemap 3.7.4 and YAML 2.9.1 |
| #13 | Sharp 0.35.5, including a newer fix beyond the proposed 0.35.4 |
| #11, #14, #17, #21 | Refreshed transitive SVGO, js-yaml, undici and devalue in the lockfile |
| #5, #16 | pytest 9.1.1 and markitdown 0.1.8 |
| #18, #20 | CodeQL init and analyze pinned to the verified v4.38.2 commit |
| #19 | Pages deploy pinned to the verified v5.0.1 commit |
| #6 | The proposed dependency-review-action v5.0.0 pin was already on main |

The [grouped bot PR](https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents/pull/15) supplied release and compatibility information; individual branches were not merged wholesale. Updates were applied together on main, preserving current project changes and choosing newer patched versions where necessary.

## Transitive correction

Refreshing compatible dependencies fixed additional findings in source-map-js, smol-toml and http-cache-semantics. Expressive Code still pulled postcss-selector-parser 6 through postcss-nested 6. The [selector parser advisory](https://github.com/advisories/GHSA-rj75-hqrm-r3gf) identifies 7.1.6 as patched. A scoped npm override selects that version only under postcss-nested; it avoids downgrading Starlight as suggested by the automatic force-fix path. Remove the override once the upstream dependency chain selects a patched parser on its own.

The Node engine floor is now 22.19.0, matching the resolved undici requirement. The existing .nvmrc version satisfies it.

## Site compatibility

Starlight now uses a native sidebar popover. The custom header button targets that popover and derives its expanded state from the actual open state. The replacement CSS hides the new default button. This preserves native dismissal and supports the custom mobile toggle without JavaScript. The [Starlight release notes](https://github.com/withastro/starlight/releases/tag/@astrojs%2Fstarlight@0.42.1) describe the sidebar transition.

## Validation

- Clean npm installation from the committed lockfile and full npm audit: zero known vulnerabilities.
- Fresh Python environment with pinned development requirements; pip-audit includes resolved transitive dependencies: zero known vulnerabilities.
- Python regression suite, site publishing tests, repository validation, site build and site integrity checks.
- Chrome checks for desktop visibility, mobile opening/closing, Escape dismissal, resize, sidebar link navigation and the native toggle with JavaScript disabled.

Audits report advisories known to their databases at verification time. They do not prove that every dependency is free of defects. GitHub alerts are verified again after the main-branch push; superseded bot PRs are closed after their changes are present.
