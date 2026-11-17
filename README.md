# Remove Padding
![Latest Version](https://img.shields.io/github/v/tag/mbeckh/picard-plugin-remove-padding?sort=semver&filter=v*&style=flat-square&label=latest)
![Supports](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmbeckh%2Fpicard-plugin-remove-padding%2Frefs%2Fheads%2Fmain%2F.works_with.yml&query=%24.picard.from&prefix=picard+%3E%3D&style=flat-square&label=supports&color=orange)
![Tested with](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmbeckh%2Fpicard-plugin-remove-padding%2Frefs%2Fheads%2Fmain%2F.works_with.yml&query=%24.picard.latest&prefix=picard+%3C%3D&style=flat-square&label=tested+with&color=green)

A plugin for [MusicBrainz Picard](https://picard.musicbrainz.org) to remove padding from ID3v2 tags.

## What it Does

The plugin runs as a file post save processor and adds a context menu action.

Processing respects the following options from Picard:
* ID3v2 version
* Save IDv1 tags
* Preserve file timestamps

## License

The code is released under the Apache License Version 2.0. Please see [LICENSE](LICENSE) for details and [NOTICE](NOTICE) for the required information when using picard-plugin-remove-padding in your own work.
