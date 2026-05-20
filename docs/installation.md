# Installation

Codex plugins are installed through a plugin marketplace. Cloning the repository is useful for development, but `git clone` plus `cd` does not install or enable the plugin by itself.

## Install From GitHub

Register this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add FarzamHejaziK/codex-investment-plugin --ref main
```

Then open Codex and install the plugin from the plugin browser:

```bash
codex
```

Inside Codex:

```text
/plugins
```

Open the **Codex Investment Plugin** marketplace, install **Codex Investment Assistant**, then start a new thread. Run:

```text
/investment-setup
```

## Install From A Local Clone

For local development:

```bash
git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git
cd codex-investment-plugin
codex plugin marketplace add .
```

Then open Codex, run `/plugins`, install the plugin from the **Codex Investment Plugin** marketplace, and start a new thread.

## Verify The Plugin Shape

From the repo:

```bash
python3 scripts/validate-plugin.py
```

The validation checks the Codex manifest, marketplace manifest, command files, safety rules, workspace bootstrap, and Claude-to-Codex conversion hygiene.

## Command Surface

After the plugin is installed and enabled, the command files under `commands/` are exposed as investment commands:

```text
/investment-setup
/investment-daily
/investment-new-strategy
/investment-help
```

The plugin can also be invoked conversationally. For example:

```text
Use the investment plugin to set up my workspace.
```
