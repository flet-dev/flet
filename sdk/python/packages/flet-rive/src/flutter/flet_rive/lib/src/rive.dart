import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:rive/rive.dart' as rive;

class RiveControl extends StatefulWidget {
  final Control control;

  const RiveControl({super.key, required this.control});

  @override
  State<RiveControl> createState() => _RiveControlState();
}

class _RiveControlState extends State<RiveControl> {
  Future<rive.File?>? _fileFuture;
  rive.File? _file;
  String? _filePath;
  bool _fileIsLocal = false;
  Map<String, String>? _fileHeaders;
  _RiveMultiAnimationPainter? _painter;
  List<String> _animations = const [];
  List<String> _stateMachines = const [];
  double _speedMultiplier = 1;
  rive.Fit _fit = rive.RiveDefaults.fit;
  Alignment _alignment = rive.RiveDefaults.alignment;

  @override
  void dispose() {
    _painter?.dispose();
    _file?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Rive build: ${widget.control.id} (${widget.control.hashCode})");
    var src = widget.control.getString("src");
    if (src == null) {
      return const ErrorControl("Rive must have \"src\" specified.");
    }

    var artBoard = widget.control.getString("art_board");
    var useArtBoardSize = widget.control.getBool("use_art_board_size", false)!;
    var boxFit = widget.control.getBoxFit("fit");
    var fit = _toRiveFit(boxFit);
    var alignment =
        widget.control.getAlignment("alignment") ?? rive.RiveDefaults.alignment;
    var placeholder = widget.control.buildWidget("placeholder");
    var speedMultiplier = widget.control.getDouble("speed_multiplier", 1)!;
    var animations = widget.control.get<List<String>>("animations", const [])!;
    var stateMachines =
        widget.control.get<List<String>>("state_machines", const [])!;
    var headers = widget.control.get("headers")?.cast<String, String>();
    var clipRect = widget.control.getRect("clip_rect");

    var assetSrc = widget.control.backend.getAssetSource(src);
    _syncFileLoader(assetSrc.path, assetSrc.isFile, headers);
    _syncPainter(
      animations: animations,
      stateMachines: stateMachines,
      speedMultiplier: speedMultiplier,
      fit: fit,
      alignment: alignment,
    );

    final fileFuture = _fileFuture;
    final painter = _painter;
    if (fileFuture == null || painter == null) {
      return ConstrainedControl(
        control: widget.control,
        child: placeholder ?? const SizedBox.shrink(),
      );
    }

    Widget riveWidget = FutureBuilder<rive.File?>(
      future: fileFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return placeholder ?? const SizedBox.shrink();
        }
        if (snapshot.hasError) {
          return ErrorControl(
              "Rive failed to load: ${snapshot.error ?? "unknown error"}");
        }
        final file = snapshot.data;
        if (file == null) {
          return const ErrorControl("Rive file could not be loaded.");
        }
        _syncLoadedFile(file);

        Widget child = rive.RiveFileWidget(
          file: file,
          painter: painter,
          artboardName: artBoard,
        );

        if (useArtBoardSize) {
          final artboard = artBoard == null
              ? file.defaultArtboard()
              : file.artboard(artBoard);
          if (artboard != null) {
            final bounds = artboard.bounds;
            child = SizedBox(
              width: bounds.width,
              height: bounds.height,
              child: child,
            );
          }
        }

        if (clipRect != null) {
          child = ClipRect(
            clipper: _RiveRectClipper(clipRect),
            child: child,
          );
        }

        return child;
      },
    );

    return ConstrainedControl(control: widget.control, child: riveWidget);
  }

  void _syncLoadedFile(rive.File file) {
    if (!identical(file, _file)) {
      _file?.dispose();
      _file = file;
    }
  }

  void _syncFileLoader(
    String path,
    bool isFile,
    Map<String, String>? headers,
  ) {
    if (_fileFuture != null &&
        _filePath == path &&
        _fileIsLocal == isFile &&
        mapEquals(_fileHeaders, headers)) {
      return;
    }
    _file?.dispose();
    _file = null;
    _filePath = path;
    _fileIsLocal = isFile;
    _fileHeaders = headers == null ? null : Map<String, String>.from(headers);
    _fileFuture = _loadFile(path, isFile, headers);
  }

  void _syncPainter({
    required List<String> animations,
    required List<String> stateMachines,
    required double speedMultiplier,
    required rive.Fit fit,
    required Alignment alignment,
  }) {
    if (_painter == null ||
        !listEquals(_animations, animations) ||
        !listEquals(_stateMachines, stateMachines)) {
      _painter?.dispose();
      _painter = _RiveMultiAnimationPainter(
        animationNames: List<String>.from(animations),
        stateMachineNames: List<String>.from(stateMachines),
        speedMultiplier: speedMultiplier,
        fit: fit,
        alignment: alignment,
      );
      _animations = List<String>.from(animations);
      _stateMachines = List<String>.from(stateMachines);
      _speedMultiplier = speedMultiplier;
      _fit = fit;
      _alignment = alignment;
      return;
    }

    if (_speedMultiplier != speedMultiplier) {
      _painter!.speedMultiplier = speedMultiplier;
      _speedMultiplier = speedMultiplier;
    }
    if (_fit != fit) {
      _painter!.fit = fit;
      _fit = fit;
    }
    if (_alignment != alignment) {
      _painter!.alignment = alignment;
      _alignment = alignment;
    }
  }

  Future<rive.File?> _loadFile(
    String path,
    bool isFile,
    Map<String, String>? headers,
  ) async {
    if (isFile) {
      return rive.File.path(
        path,
        riveFactory: rive.Factory.rive,
      );
    }
    return rive.File.url(
      path,
      riveFactory: rive.Factory.rive,
      headers: headers,
    );
  }
}

base class _RiveMultiAnimationPainter extends rive.BasicArtboardPainter
    with rive.RivePointerEventMixin {
  _RiveMultiAnimationPainter({
    required List<String> animationNames,
    required List<String> stateMachineNames,
    required this.speedMultiplier,
    required super.fit,
    required super.alignment,
  })  : _animationNames = animationNames,
        _stateMachineNames = stateMachineNames,
        super();

  final List<String> _animationNames;
  final List<String> _stateMachineNames;
  double speedMultiplier;
  final List<rive.Animation> _animations = [];
  final List<rive.StateMachine> _stateMachines = [];
  final List<rive.CallbackHandler> _inputHandlers = [];
  bool _previousHit = false;

  @override
  void artboardChanged(rive.Artboard artboard) {
    super.artboardChanged(artboard);
    _disposeControllers();

    if (_animationNames.isEmpty && _stateMachineNames.isEmpty) {
      final machine = artboard.defaultStateMachine();
      if (machine != null) {
        _stateMachines.add(machine);
        _inputHandlers.add(machine.onInputChanged(_onInputChanged));
      } else if (artboard.animationCount() > 0) {
        _animations.add(artboard.animationAt(0));
      }
    } else {
      for (final name in _animationNames) {
        final animation = artboard.animationNamed(name);
        if (animation != null) {
          _animations.add(animation);
        }
      }

      for (final name in _stateMachineNames) {
        final machine = artboard.stateMachine(name);
        if (machine != null) {
          _stateMachines.add(machine);
          _inputHandlers.add(machine.onInputChanged(_onInputChanged));
        }
      }
    }

    notifyListeners();
  }

  void _onInputChanged(int inputId) {
    notifyListeners();
  }

  @override
  bool hitTest(Offset position) {
    if (_stateMachines.isEmpty || artboard == null) {
      return false;
    }
    final hit = _stateMachines.any((machine) {
      return machine.hitTest(
        localToArtboard(
          position: position,
          artboardBounds: artboard!.bounds,
          fit: fit,
          alignment: alignment,
          size: size,
          scaleFactor: layoutScaleFactor,
        ),
      );
    });
    return hit || _previousHit;
  }

  @override
  void pointerEvent(PointerEvent event, HitTestEntry entry) {
    if (_stateMachines.isEmpty || artboard == null) {
      return;
    }
    var hit = false;
    for (final machine in _stateMachines) {
      final position = localToArtboard(
        position: event.localPosition,
        artboardBounds: artboard!.bounds,
        fit: fit,
        alignment: alignment,
        size: size,
        scaleFactor: layoutScaleFactor,
      );
      final rive.HitResult result;
      if (event is PointerDownEvent) {
        result = machine.pointerDown(position, pointerId: event.pointer);
      } else if (event is PointerUpEvent) {
        result = machine.pointerUp(position, pointerId: event.pointer);
      } else if (event is PointerMoveEvent) {
        result = machine.pointerMove(position, pointerId: event.pointer);
      } else if (event is PointerHoverEvent) {
        result = machine.pointerMove(position, pointerId: event.pointer);
      } else if (event is PointerExitEvent) {
        result = machine.pointerExit(position, pointerId: event.pointer);
      } else {
        result = rive.HitResult.none;
      }
      if (result != rive.HitResult.none) {
        hit = true;
      }
    }
    if (hit || _previousHit) {
      scheduleRepaint();
    }
    _previousHit = hit;
  }

  @override
  bool advance(double elapsedSeconds) {
    if (_animations.isEmpty && _stateMachines.isEmpty) {
      final artboard = this.artboard;
      if (artboard == null) {
        return false;
      }
      final scaled = elapsedSeconds * speedMultiplier;
      return artboard.advance(scaled) || artboard.updatePass();
    }

    var advanced = false;
    final scaled = elapsedSeconds * speedMultiplier;
    for (final animation in _animations) {
      advanced = animation.advanceAndApply(scaled) || advanced;
    }
    for (final machine in _stateMachines) {
      advanced = machine.advanceAndApply(scaled) || advanced;
    }
    return advanced;
  }

  void _disposeControllers() {
    for (final animation in _animations) {
      animation.dispose();
    }
    _animations.clear();
    for (final machine in _stateMachines) {
      machine.dispose();
    }
    _stateMachines.clear();
    for (final handler in _inputHandlers) {
      handler.dispose();
    }
    _inputHandlers.clear();
  }

  @override
  void dispose() {
    _disposeControllers();
    super.dispose();
  }
}

class _RiveRectClipper extends CustomClipper<Rect> {
  _RiveRectClipper(this.rect);

  final Rect rect;

  @override
  Rect getClip(Size size) => rect;

  @override
  bool shouldReclip(covariant _RiveRectClipper oldClipper) {
    return oldClipper.rect != rect;
  }
}

rive.Fit _toRiveFit(BoxFit? fit) {
  return switch (fit) {
    BoxFit.fill => rive.Fit.fill,
    BoxFit.contain => rive.Fit.contain,
    BoxFit.cover => rive.Fit.cover,
    BoxFit.fitHeight => rive.Fit.fitHeight,
    BoxFit.fitWidth => rive.Fit.fitWidth,
    BoxFit.none => rive.Fit.none,
    BoxFit.scaleDown => rive.Fit.scaleDown,
    _ => rive.RiveDefaults.fit,
  };
}
