---
title: "Flet protocol framing upgraded for DataChannel support"
---

# Flet protocol framing upgraded for DataChannel support

:::note
This guide is accurate as of Flet 0.86.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.86.0 introduces dedicated **data channels** for widgets that need to
move bulk binary data (image frames, audio buffers, ML tensors) between Dart
and Python without going through the MsgPack control protocol.

Enabling this required a one-time upgrade of the Flet protocol's wire format:

- **Stream-oriented transports** (`flet run` dev mode over UDS / TCP) now use
  **4-byte little-endian length-prefixed framing**. The previous streaming
  `msgpack.Unpacker.feed` decode is gone.
- **Every transport** (sockets, WebSocket, `dart_bridge` FFI, Pyodide
  `postMessage`) now puts a **1-byte type discriminator** at the head of each
  packet:
  - `0x00` — MsgPack-encoded Flet control frame (widget state, events) — same
    contents as before, just with a type byte in front.
  - `0x01` — raw DataChannel frame (`[channel_id:u32 LE][payload]`).

The new format is **not backwards-compatible**: a Flet 0.85 client cannot talk
to a Flet 0.86 server, and vice versa. The `flet-cli` dev server and the
in-process Python runtime were upgraded together in this release.

## Background

Flet's previous wire format on UDS / TCP relied on `msgpack.Unpacker.feed` to
re-assemble messages from arbitrary byte-stream chunks. That works for
MsgPack-only traffic but doesn't compose with a second logical stream of raw
bytes — you can't tell a partial MsgPack value from the start of a raw frame
without an out-of-band marker.

Adding the 1-byte type byte + 4-byte length prefix solves this in the smallest
possible way:

- Receivers read `[length][type][...]`, fan out by type byte, no streaming
  decoder state to maintain.
- Message-oriented transports (WebSocket, `postMessage`, `dart_bridge`) drop
  the length prefix since each message is already one packet; they keep the
  type byte.
- Per-frame overhead is 5 bytes (message-oriented) or 9 bytes (stream-oriented)
  — under 1% at any payload size that motivates a data channel.

## Migration guide

### Most users — nothing to change

If you only use `flet build` artifacts or run `flet run` with the matching
`flet` package version (the default install pulls both at once), there's
nothing to do. The CLI and the runtime are version-locked.

### Users running `flet-cli` and the `flet` Python package from different installs

Make sure both come from the same release. The common gotcha is a global
`flet` install plus a project-local `flet` in `.venv` at different versions
— upgrade or pin both to ≥ `0.86.0` (or both to ≤ `0.85.x`).

A version mismatch will surface as a connection failure during `flet run`
with a parse error in the dev-server log.

### Users with custom backends or sidecars speaking the Flet protocol

The wire format changed. Update your encoder/decoder:

- **Inbound on a stream transport** (UDS / TCP): read 4 bytes (length, u32 LE),
  read that many bytes, the first byte is the type discriminator, the rest is
  the payload.
- **Inbound on a message transport** (WebSocket, `postMessage`): each
  message's first byte is the type discriminator, the rest is the payload.
- **Outbound**: same shape, mirrored.

Treat `0x01` (raw DataChannel) frames as opaque if you don't use data channels
— forward them along or drop them, never feed them to your MsgPack decoder.

### Code that depended on `StreamingMsgpackDeserializer`

The Dart-side class `package:flet/src/transport/streaming_msgpack_deserializer.dart`
is removed. There are no public consumers — it was an internal helper for
stream-transport framing that's no longer needed now that every packet is
length-delimited. If you imported it (you shouldn't have), decode each inbound
buffer with one-shot `msgpack.deserialize(bytes)` instead.

### Custom widgets that override `MatplotlibChartCanvas`

`MatplotlibChartCanvas` now transports its `apply_full` / `apply_diff` /
`clear` frames through a [DataChannel] rather than `_invoke_method` arguments.
The Python-facing method signatures are unchanged (`apply_full(image_bytes:
bytes)`, etc.), and they remain the documented API. But if you subclassed the
canvas and overrode the Dart-side `_invokeMethod` handler, that override no
longer fires — the Dart side now consumes a 1-byte opcode + PNG payload from
the channel directly.

## Timeline

- Changed in: `0.86.0`

## References

- API: `flet.DataChannel` (Python) and `FletBackend.openDataChannel` (Dart) — see the module docstrings in `flet/data_channel.py`; dedicated reference pages will be added in a follow-up.
- Release notes: [Flet 0.86.0](../../release-notes.md)
