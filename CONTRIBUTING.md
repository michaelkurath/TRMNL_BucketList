# Contributing

Thanks for helping improve the TRMNL Bucket List recipe.

## Before opening a pull request

1. Keep changes focused and explain the problem they solve.
2. Preview every affected layout in TRMNL: full, half-horizontal, half-vertical, and quadrant.
3. Test both Focus and List modes.
4. Test completed-item visibility with the setting enabled and disabled.
5. Check that the result remains readable on a monochrome e-ink display.
6. Do not commit credentials, personal bucket-list content, or private TRMNL configuration.

## Design guidelines

- Prefer high contrast and clear visual hierarchy.
- Avoid small, thin, or low-contrast text and lines.
- Never nest a `.layout` container inside another `.layout`; use flex, grid, or columns inside the outer layout.
- Keep the recipe static and avoid unnecessary external browser dependencies.
- Preserve all four supported layouts when changing display logic.

## Reporting problems

Open a GitHub issue with the affected layout, TRMNL device or resolution, selected display mode, relevant settings, a screenshot if possible, and clear reproduction steps. Remove personal bucket-list content before sharing screenshots or examples.

By contributing, you agree that your contribution may be distributed under the project's Creative Commons Attribution 4.0 International License (CC BY 4.0).
