project(
  'FIU-Luna0', 'cpp',
  version: '0.1.0',
  default_options: ['cpp_std=c++17']
)

# normal dependencies
boost_dep = dependency('boost', modules: ['system', 'thread'])
protobuf_dep = dependency('protobuf')
grpc_dep = dependency('grpc++')
libevdev_dep = dependency('libevdev')

# proto & grpc
protoc = find_program('protoc')
proto_input = files('proto/luna.proto')
proto_target = custom_target(
  'luna_proto',
  input: proto_input,
  output: [
    'luna.pb.cc',
    'luna.pb.h',
    'luna.grpc.pb.cc',
    'luna.grpc.pb.h'
  ],
  command: [
    protoc,
    '--proto_path=../proto',
    '--grpc_out=.',
    '--cpp_out=.',
    '--plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin',
    '@INPUT@',
  ],
  install: false,
  build_by_default: true,
)

proto_inc = include_directories('proto')

# declare proto as a dependency
luna_proto_dep = declare_dependency(
  sources: proto_target,
  include_directories: proto_inc
)

shared_dependencies = [
  boost_dep,
  protobuf_dep,
  grpc_dep,
  libevdev_dep,
  luna_proto_dep,
]

# server details
server_sources = [
  'src/server.cpp',
  'src/network/network.cpp',
  'src/controller/controller.cpp',
  'src/utils/utils.cpp'
]

server_dependencies = shared_dependencies + []

# client details
client_sources = [
  'src/client.cpp',
  'src/network/network.cpp',
  'src/controller/controller.cpp',
  'src/utils/utils.cpp'
]

client_dependencies = shared_dependencies + []

## executables
executable(
  'client',
  sources: client_sources,
  dependencies: client_dependencies,
  include_directories: include_directories('src'),
  install: false,
)

executable(
  'server',
  sources: server_sources,
  dependencies: server_dependencies,
  include_directories: include_directories('src'),
  install: false,
)
