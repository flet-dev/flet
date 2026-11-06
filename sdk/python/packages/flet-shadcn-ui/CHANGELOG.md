# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 1.1.2

### Changed

- Web apps load Lucide's and Geist's fonts when the first shadcn control or Lucide icon is built, not before the app's first frame; `flet build web` leaves out Lucide's unused weight fonts ([#PR](https://github.com/flet-dev/flet/pull/PR)) by @FeodorFitsner.

## 1.1.0

### Added

- Initial release: controls styled after [shadcn/ui](https://ui.shadcn.com), built on the Flutter [`shadcn_ui`](https://pub.dev/packages/shadcn_ui) package, with `Theme` color schemes and the [Lucide](https://lucide.dev) icon set (`LucideIcons`). Includes `Button`, `IconButton`, `Badge`, `Alert`, `Avatar`, `Card`, `Breadcrumb`, `Separator`, `Progress`, `Input`, `Textarea`, `Checkbox`, `Switch`, `Slider`, `RadioGroup`, `Select`, `InputOTP`, `Calendar`, `DatePicker`, `DateRangePicker`, `TimePicker`, `Tabs`, `Accordion`, `ResizablePanelGroup`, `Tooltip`, `Popover`, `ContextMenu`, `Menubar`, `Table`, `Dialog`, `Sheet`, `Toast` and `Sonner` ([#6918](https://github.com/flet-dev/flet/pull/6918)) by @InesaFitsner.
