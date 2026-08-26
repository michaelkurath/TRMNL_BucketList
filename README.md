# TRMNL Bucket List

An unofficial, open-source [TRMNL](https://trmnl.com/) recipe that keeps personal goals, dreams, places, projects, and experiences visible on an e-ink display.

<img width="150" alt="Works with TRMNL" src="https://trmnl.com/images/brand/badges/light/works-with-trmnl/trmnl-badge-works-with-light.svg" />

## Features

- Focus mode highlights one random open item
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

## Contributing

Bug reports and focused improvements are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.

## License and attribution

The original visual design, data parsing logic, markup, and other original content in this repository are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](./LICENSE), in accordance with the [TRMNL Community Plugin License](https://trmnl.com/plugin-license).

When sharing or adapting the recipe, credit Michael Kurath, link to this repository and the CC BY 4.0 license, and indicate whether changes were made.

TRMNL and its associated names and trademarks remain the property of their respective owners. This repository is an independent community project and is not affiliated with or endorsed by TRMNL.
