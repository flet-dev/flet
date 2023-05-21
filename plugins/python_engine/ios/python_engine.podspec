#
# To learn more about a Podspec see http://guides.cocoapods.org/syntax/podspec.html.
# Run `pod lib lint python_engine.podspec` to validate before publishing.
#
Pod::Spec.new do |s|
  s.name             = 'python_engine'
  s.version          = '0.0.1'
  s.summary          = 'A new Flutter plugin project.'
  s.description      = <<-DESC
A new Flutter plugin project.
                       DESC
  s.homepage         = 'http://example.com'
  s.license          = { :file => '../LICENSE' }
  s.author           = { 'Your Company' => 'email@example.com' }
  s.source           = { :path => '.' }
  s.source_files = 'Classes/**/*'
  s.dependency 'Flutter'
  s.platform = :ios, '12.0'

  # Flutter.framework does not contain a i386 slice.
  s.pod_target_xcconfig = { 'DEFINES_MODULE' => 'YES', 'EXCLUDED_ARCHS[sdk=iphonesimulator*]' => 'i386' }
  s.swift_version = '5.0'

  s.prepare_command = <<-CMD
    PYTHON_DIST_FILENAME="Python-3.11-iOS-support.b1.tar.gz"
    curl -sLO https://github.com/beeware/Python-Apple-support/releases/download/3.11-b1/$PYTHON_DIST_FILENAME
    tar -zxvf $PYTHON_DIST_FILENAME -C Frameworks
    cp module.modulemap Frameworks/Python.xcframework/ios-arm64/Headers
    cp module.modulemap Frameworks/Python.xcframework/ios-arm64_x86_64-simulator/Headers
    rm $PYTHON_DIST_FILENAME
CMD
  s.vendored_frameworks = 'Frameworks/Python.xcframework'
  s.resource = ['Frameworks/python-stdlib', 'Frameworks/platform-site']
end
