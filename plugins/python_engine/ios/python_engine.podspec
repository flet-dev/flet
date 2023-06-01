#
# To learn more about a Podspec see http://guides.cocoapods.org/syntax/podspec.html.
# Run `pod lib lint python_engine.podspec` to validate before publishing.
#
Pod::Spec.new do |s|
  s.name             = 'python_engine'
  s.version          = '0.1.0'
  s.summary          = 'A new Flutter plugin project.'
  s.description      = <<-DESC
A new Flutter plugin project.
                       DESC
  s.homepage         = 'http://example.com'
  s.license          = { :file => '../LICENSE' }
  s.author           = { 'Your Company' => 'email@example.com' }
  s.source           = { :path => '.' }
  #s.static_framework = true
  s.source_files = ['Classes/**/*']
  s.dependency 'Flutter'
  s.platform = :ios, '12.0'

  # Flutter.framework does not contain a i386 slice.
  s.pod_target_xcconfig = {
    'DEFINES_MODULE' => 'YES',
    'EXCLUDED_ARCHS[sdk=iphonesimulator*]' => 'arm64',
    'OTHER_LDFLAGS' => '-ObjC -all_load -lc++'
  }
  s.swift_version = '5.0'

  python_framework = 'dist/frameworks/Python.xcframework'
  s.prepare_command = <<-CMD
    rm -rf #{python_framework}
    mkdir -p #{python_framework}
    cp -R pod_templates/Python.xcframework/* #{python_framework}
    cp dist/lib/libpython3.a #{python_framework}/ios-arm64
    cp dist/lib/libpython3.a #{python_framework}/ios-arm64_x86_64-simulator
    cp -R dist/root/python3/include/python3.10/* #{python_framework}/ios-arm64/Headers
    cp -R dist/root/python3/include/python3.10/* #{python_framework}/ios-arm64_x86_64-simulator/Headers

    # fix import subprocess, asyncio
    cp -R pod_templates/site-packages/* dist/root/python3/lib/python3.10/site-packages
CMD

  s.libraries = 'z', 'bz2', 'c++', 'sqlite3'
  s.vendored_libraries = 'dist/lib/*.a'
  s.vendored_frameworks = python_framework
  s.resource = ['dist/root/python3/lib']
end
