# TRMNL Bucket List

An unofficial, open-source [TRMNL](https://trmnl.com/) recipe that keeps personal goals, dreams, places, projects, and experiences visible on an e-ink display.

<img width="150" alt="Works with TRMNL" src="https://trmnl.com/images/brand/badges/light/works-with-trmnl/trmnl-badge-works-with-light.svg" />

## Features

- Focus mode highlights one random eligible item (completed items are included when enabled)
- List mode shows several open and completed items
- Optional completed-item visibility
- Configurable list length
- Full-screen, half-horizontal, half-vertical, and quadrant layouts
- Static recipe with no external service or account dependency
- Licensed for sharing and adaptation under CC BY 4.0

## Item format

Enter one item per line in the recipe settings:

```text
[ ] See the northern lights | Travel | Winter trip idea
[x] Build a home server | Projects | Done
[ ] Visit Japan | Travel | Food, trains, design
```

The category and note are optional. Use `[x]` for completed items and `[ ]` for open items. Plain titles also work.

## Repository structure

```text
src/
  full.liquid            Full-screen layout
  half_horizontal.liquid Horizontal half-screen layout
  half_vertical.liquid   Vertical half-screen layout
  quadrant.liquid        Quadrant layout
  settings.yml           TRMNL recipe configuration
```

## Development

Templates and settings in [`src/`](./src/) can be previewed locally with [trmnlp](https://github.com/usetrmnl/trmnlp):

```sh
gem install trmnl_preview
trmnlp serve
```

Preview all four layouts and test both display modes before submitting changes. TRMNL layouts must not be nested; use flex, grid, or columns inside the outer `.layout` container.

### Readability and regression tests

List mode uses standard `title` and `description` sizes on OG, with `lg:title--large` and `lg:description--large` on X. Quadrants display item names only. The overflow engine uses the actual layout height; when the selected items cannot fit, an "and N more" counter is shown rather than shrinking the text. Long titles and descriptions are each clamped to one line so rows remain predictable across all view sizes.

With Docker available, run from the repository root:

```sh
docker run --rm -v "$PWD:/plugin" trmnl/trmnlp lint
python3 scripts/trmnlp_qa.py
```

The GitHub Actions workflow runs the same tests when source or test files change. It checks toggle representations, empty/all-completed states, Focus mode, and item limits, and generates OG/X/portrait screenshots for 5-item, 12-item, and long-text lists. A test-only capture hook waits for `TRMNL_PLUGINS_READY` before TRMNLP captures the PNG and records visible-item geometry; the suite rejects rows outside the layout. This hook is not recipe markup and does not change the framework. Screenshot generation is followed by manual visual review; a green workflow does not itself certify visual quality. Artifacts remain available for 30 days.

Import the latest GitHub version into TRMNL before saving changes in its editor: exporting a stale TRMNL copy can overwrite newer repository templates.

## Contributing

Bug reports and focused improvements are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.

## License and attribution

The original visual design, data parsing logic, markup, and other original content in this repository are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](./LICENSE), in accordance with the [TRMNL Community Plugin License](https://trmnl.com/plugin-license).

When sharing or adapting the recipe, credit Michael Kurath, link to this repository and the CC BY 4.0 license, and indicate whether changes were made.

TRMNL and its associated names and trademarks remain the property of their respective owners. This repository is an independent community project and is not affiliated with or endorsed by TRMNL.
