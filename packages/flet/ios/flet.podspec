Pod::Spec.new do |s|
  s.name             = 'flet'
  s.version          = '1.1.4'
  s.summary          = 'Flet Flutter package with native WebAuth support'
  s.description      = 'Flet core Flutter package'
  s.homepage         = 'https://flet.dev'
  s.license          = { :file => '../LICENSE' }
  s.author           = { 'Flet' => 'hello@flet.dev' }
  s.source           = { :path => '.' }
  s.source_files = 'Classes/**/*'
  s.dependency 'Flutter'
  s.platform = :ios, '12.0'
  s.pod_target_xcconfig = { 'DEFINES_MODULE' => 'YES' }
  s.swift_version = '5.0'
end
