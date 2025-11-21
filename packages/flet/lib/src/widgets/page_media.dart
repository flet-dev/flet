import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../protocol/page_media_data.dart';
import '../utils/debouncer.dart';

class PageMedia extends StatefulWidget {
  final Control? view;
  const PageMedia({super.key, this.view});

  @override
  State<PageMedia> createState() => _PageMediaState();
}

class _PageMediaState extends State<PageMedia> {
  final _debouncer = Debouncer(milliseconds: 100);

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  _onPageSizeChanged(bool pageSizeUpdated, Size newSize) {
    var backend = FletBackend.of(context);
    if (pageSizeUpdated) {
      _debouncer.run(() {
        backend.updatePageSize(newSize, view: widget.view);
      });
    } else {
      backend.updatePageSize(newSize, view: widget.view);
    }
  }

  _onPlatformBrightnessChanged(Brightness newBrightness) {
    FletBackend.of(context).updateBrightness(newBrightness);
  }

  _onMediaChanged(PageMediaData newMedia) {
    FletBackend.of(context).updateMedia(newMedia, view: widget.view);
  }

  @override
  Widget build(BuildContext context) {
    FletBackend backend = FletBackend.of(context);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      var pageSizeUpdated = backend.pageSizeUpdated.isCompleted;

      var platformBrightness = MediaQuery.platformBrightnessOf(context);
      if (platformBrightness != backend.platformBrightness ||
          !pageSizeUpdated) {
        _onPlatformBrightnessChanged(platformBrightness);
      }

      var newMedia = PageMediaData(
        padding: PaddingData(MediaQuery.paddingOf(context)),
        viewPadding: PaddingData(MediaQuery.viewPaddingOf(context)),
        viewInsets: PaddingData(MediaQuery.viewInsetsOf(context)),
        devicePixelRatio: MediaQuery.devicePixelRatioOf(context),
        orientation: MediaQuery.orientationOf(context),
        alwaysUse24HourFormat: MediaQuery.alwaysUse24HourFormatOf(context),
      );

      if (newMedia != backend.media || !pageSizeUpdated) {
        _onMediaChanged(newMedia);
      }

      var pageSize = MediaQuery.sizeOf(context);
      if (pageSize != backend.pageSize) {
        _onPageSizeChanged(pageSizeUpdated, pageSize);
      }
    });

    return const SizedBox.shrink();
  }
}
