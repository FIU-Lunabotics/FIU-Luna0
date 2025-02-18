// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: proto/luna.proto

#include "proto/luna.pb.h"
#include "proto/luna.grpc.pb.h"

#include <functional>
#include <grpcpp/support/async_stream.h>
#include <grpcpp/support/async_unary_call.h>
#include <grpcpp/impl/channel_interface.h>
#include <grpcpp/impl/client_unary_call.h>
#include <grpcpp/support/client_callback.h>
#include <grpcpp/support/message_allocator.h>
#include <grpcpp/support/method_handler.h>
#include <grpcpp/impl/rpc_service_method.h>
#include <grpcpp/support/server_callback.h>
#include <grpcpp/impl/server_callback_handlers.h>
#include <grpcpp/server_context.h>
#include <grpcpp/impl/service_type.h>
#include <grpcpp/support/sync_stream.h>
namespace luna {

static const char* Controller_method_names[] = {
  "/luna.Controller/SendEvent",
};

std::unique_ptr< Controller::Stub> Controller::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< Controller::Stub> stub(new Controller::Stub(channel, options));
  return stub;
}

Controller::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options)
  : channel_(channel), rpcmethod_SendEvent_(Controller_method_names[0], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status Controller::Stub::SendEvent(::grpc::ClientContext* context, const ::luna::ControllerEvent& request, ::luna::Empty* response) {
  return ::grpc::internal::BlockingUnaryCall< ::luna::ControllerEvent, ::luna::Empty, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_SendEvent_, context, request, response);
}

void Controller::Stub::async::SendEvent(::grpc::ClientContext* context, const ::luna::ControllerEvent* request, ::luna::Empty* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::luna::ControllerEvent, ::luna::Empty, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_SendEvent_, context, request, response, std::move(f));
}

void Controller::Stub::async::SendEvent(::grpc::ClientContext* context, const ::luna::ControllerEvent* request, ::luna::Empty* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_SendEvent_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::luna::Empty>* Controller::Stub::PrepareAsyncSendEventRaw(::grpc::ClientContext* context, const ::luna::ControllerEvent& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::luna::Empty, ::luna::ControllerEvent, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_SendEvent_, context, request);
}

::grpc::ClientAsyncResponseReader< ::luna::Empty>* Controller::Stub::AsyncSendEventRaw(::grpc::ClientContext* context, const ::luna::ControllerEvent& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncSendEventRaw(context, request, cq);
  result->StartCall();
  return result;
}

Controller::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      Controller_method_names[0],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< Controller::Service, ::luna::ControllerEvent, ::luna::Empty, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](Controller::Service* service,
             ::grpc::ServerContext* ctx,
             const ::luna::ControllerEvent* req,
             ::luna::Empty* resp) {
               return service->SendEvent(ctx, req, resp);
             }, this)));
}

Controller::Service::~Service() {
}

::grpc::Status Controller::Service::SendEvent(::grpc::ServerContext* context, const ::luna::ControllerEvent* request, ::luna::Empty* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace luna

