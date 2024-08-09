dart pub global activate fvm
export PATH=$HOME/.pub-cache/bin:$HOME/fvm/default/bin:$PATH
fvm install $FLUTTER_VERSION
fvm global $FLUTTER_VERSION
flutter --version