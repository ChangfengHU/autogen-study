# Topics

This document describes the semantics and components of publishing messages and subscribing to topics.

## Overview

Topics are used as the primitive to manage which agents receive a given published message. Agents subscribe to topics. There is an application defined mapping from topic to agent instance.

These concepts intentionally map to the [CloudEvents](https://cloudevents.io/) specification. This allows for easy integration with existing systems and tools.

### Non-goals

This document does not specify RPC/direct messaging

## Identifiers

A topic is identified by two components (called a `TopicId`):# 主题

本文档描述了发布消息和订阅主题的语义和组件。

## 概述

主题被用作管理哪些代理接收给定发布消息的基元。代理订阅主题。从主题到代理实例有一个应用定义的映射。

这些概念有意映射到 [CloudEvents](https://cloudevents.io/) 规范。这样可以轻松地与现有系统和工具集成。

### 非目标

本文档不指定 RPC/直接消息传递

## 标识符

主题由两个组件（称为 `TopicId`）标识：

- [`type`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type) - 表示事件类型，这是静态的并在代码中定义
  - 应使用反向域名表示法以避免命名冲突。例如：`com.example.my-topic`。
  - 允许的值必须匹配正则表达式：`^[\w\-\.\:\=]+\Z`
  - 值得注意的是，这与代理类型相同，只是增加了 `=` 和 `:` 字符
- [`source`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1) - 表示事件的来源，这是动态的并基于消息本身
  - 应为 URI

代理实例由两个组件（称为 `AgentId`）标识：

- `type` - 表示代理的类型，这是静态的并在代码中定义
  - 允许的值必须匹配正则表达式：`^[\w\-\.]+\Z`
- `key` - 表示代理类型的实例的键
  - 应为 URI

例如：`GraphicDesigner:1234`

## 订阅

订阅定义了哪些代理接收发布到主题的消息。订阅是动态的，可以随时添加或删除。

一个订阅定义了两件事：

- 类型为 `TopicId -> bool` 的匹配器函数，告诉我们“这个订阅是否与这个主题匹配”
- 类型为 `TopicId -> AgentId` 的映射器函数，告诉我们“给定这个订阅与这个主题匹配，它映射到哪个代理”

这些函数必须不带有副作用，以便评估可以被缓存。

### 代理实例创建

如果收到映射到尚不存在的代理的主题上的消息，则运行时将实例化一个代理来满足请求。

## 消息类型

代理能够处理某些类型的消息。这是代理实现的内部细节。通道中的所有代理都将接收所有消息，但会忽略它无法处理的消息。

> [!NOTE]
> 基于扩展和性能考虑，这可能会重新审视。

## 知名主题类型

代理应通过前缀订阅 `{AgentType}:` 主题作为代理类型的直接消息通道。

对于此订阅，源应直接映射到代理键。

因此，此订阅将接收以下知名主题的所有事件：

- `{AgentType}:` - 通用目的的直接消息。这些应路由到适当的消息处理程序。
- `{AgentType}:rpc_request={RequesterAgentType}` - RPC 请求消息。这些应路由到适当的 RPC 处理程序，并使用 RequesterAgentType 发布响应
- `{AgentType}:rpc_response={RequestId}` - RPC 响应消息。这些应路由回调用者的响应 future。
- `{AgentType}:error={RequestId}` - 与给定请求对应的错误消息。

- [`type`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type) - represents the type of event that occurs, this is static and defined in code
  - SHOULD use reverse domain name notation to avoid naming conflicts. For example: `com.example.my-topic`.
  - Allowed values MUST match the regex: `^[\w\-\.\:\=]+\Z`
  - Notably, this is the same as agent type with the addition of `=` and `:` characters
- [`source`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1) - represents where the event originated from, this is dynamic and based on the message itself
  - SHOULD be a URI

Agent instances are identified by two components (called an `AgentId`):

- `type` - represents the type of agent, this is static and defined in code
  - Allowed values MUST match the regex: `^[\w\-\.]+\Z`
- `key` - represents the instance of the agent type for the key
  - SHOULD be a URI

For example: `GraphicDesigner:1234`

## Subscriptions

Subscriptions define which agents receive messages published to a topic. Subscriptions are dynamic and can be added or removed at any time.

A subscription defines two things:

- Matcher func of type `TopicId -> bool`, telling us "does this subscription match this topic"
- Mapper func of type `TopicId -> AgentId`, telling us "given this subscription matches this topic, which agent does it map to"

These functions MUST be be free of side effects such that the evaluation can be cached.

### Agent instance creation

If a message is received on a topic that maps to an agent that does not yet exist the runtime will instantiate an agent to fullfil the request.

## Message types

Agents are able to handle certain types of messages. This is an internal detail of an agent's implementation. All agents in a channel will receive all messages, but will ignore messages that it cannot handle.

> [!NOTE]
> This might be revisited based on scaling and performance considerations.

## Well known topic types

Agents should subscribe via a prefix subscription to the `{AgentType}:` topic as a direct message channel for the agent type.

For this subscription source should map directly to agent key.

This subscription will therefore receive all events for the following well known topics:

- `{AgentType}:` - General purpose direct messages. These should be routed to the appropriate message handler.
- `{AgentType}:rpc_request={RequesterAgentType}` - RPC request messages. These should be routed to the appropriate RPC handler, and RequesterAgentType used to publish the response
- `{AgentType}:rpc_response={RequestId}` - RPC response messages. These should be routed back to the response future of the caller.
- `{AgentType}:error={RequestId}` - Error message that corresponds to the given request.
