import 'package:flet/src/models/boot_status.dart';
import 'package:flet/src/widgets/flet_boot_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('renders a startup error once one is set', (tester) async {
    final status =
        ValueNotifier<BootStatus>(const BootStatus(BootStage.startingUp));
    addTearDown(status.dispose);

    await tester.pumpWidget(MaterialApp(
        home: FletBootScreen(options: const {}, status: status)));

    // Nothing to show while loading: no spinner is configured by default.
    expect(find.textContaining("Error"), findsNothing);

    status.value =
        const BootStatus(BootStage.startingUp, error: "Boom: no such module");
    await tester.pump();

    expect(find.text("Error running app"), findsOneWidget);
    expect(find.textContaining("Boom: no such module"), findsOneWidget);
  });
}
