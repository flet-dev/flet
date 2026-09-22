// Run with: node --test packages/flet/test/transport/javascript_worker_transfer_test.mjs
import assert from "node:assert/strict";
import { once } from "node:events";
import { readFile } from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";
import { MessageChannel } from "node:worker_threads";

const root = new URL("../../../../", import.meta.url);
const transports = [
    "client/web/python.js",
    "sdk/python/templates/build/{{cookiecutter.out_dir}}/web/python.js",
];

for (const path of transports) {
    for (const subview of [false, true]) {
        test(`${path}: transfers ${subview ? "a subview" : "a packet"}`, async () => {
            const { port1, port2 } = new MessageChannel();
            try {
                const context = vm.createContext({
                    document: { URL: "https://example.test/" },
                    worker: port1,
                });
                vm.runInContext(await readFile(new URL(path, root), "utf8"), context);
                vm.runInContext('_apps.test = { worker };', context);

                // A view must preserve its offset and length at the receiver,
                // while transferring ownership of its entire backing buffer.
                const storage = new Uint8Array([9, 1, 2, 3, 8]);
                const packet = subview ? storage.subarray(1, 4) : storage;
                const expected = Array.from(packet);
                const offset = packet.byteOffset;
                const received = once(port2, "message");
                await context.jsSend("test", packet);

                assert.equal(packet.buffer.byteLength, 0, "message buffer must detach");
                const [message] = await received;
                assert.deepEqual(Array.from(message), expected);
                assert.equal(message.byteOffset, offset);
            } finally {
                port1.close();
                port2.close();
            }
        });
    }
}
