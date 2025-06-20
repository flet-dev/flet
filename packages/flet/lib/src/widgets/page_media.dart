import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../protocol/page_media_data.dart';
import '../utils/debouncer.dart';

class PageMedia extends StatefulWidget {
  const PageMedia({super.key});

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
        backend.updatePageSize(newSize);
      });
    } else {
      backend.updatePageSize(newSize);
    }
  }

  _onPlatformBrightnessChanged(Brightness newBrightness) {
    FletBackend.of(context).updateBrightness(newBrightness);
  }

  _onMediaChanged(PageMediaData newMedia) {
    FletBackend.of(context).updateMedia(newMedia);
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

      var padding = MediaQuery.paddingOf(context);
      var viewPadding = MediaQuery.viewPaddingOf(context);
      var viewInsets = MediaQuery.viewInsetsOf(context);
      var newMedia = PageMediaData(
          padding: PaddingData(padding),
          viewPadding: PaddingData(viewPadding),
          viewInsets: PaddingData(viewInsets));

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
