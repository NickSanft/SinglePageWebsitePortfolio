## Overview

Project Alpha is a full-stack task management platform built to explore real-time collaboration patterns and modern state synchronization. The goal was to ship something that *felt* instantaneous even on flaky connections — a benchmark for how every other tool I build should respond.

## The problem

Existing task tools fell into two camps: heavyweight enterprise platforms with deep feature trees, or single-user todo apps that broke down the moment a second person joined. I wanted to find the middle ground — multiplayer-first, but small enough that one person could grasp the whole system in an afternoon.

> The constraint that mattered: **no operation should ever feel slow, even when the network is slow.**

## Approach

I built around three principles:

1. **Optimistic UI by default.** Every mutation applies locally first, then reconciles with the server.
2. **CRDTs over locks.** Concurrent edits to the same task merge cleanly without "user X is editing" banners.
3. **One source of truth per surface.** Each view owns its data; cross-cutting concerns live in a thin coordinator.

### Stack

- **Frontend:** React + Zustand for local state, with a custom sync layer wrapping a websocket
- **Backend:** Node + Express, websocket fan-out via Redis pub/sub
- **Storage:** MongoDB for documents, with append-only event logs per workspace

## What I learned

Three things stuck with me from this build:

- **Optimistic UI is mostly a UX problem, not a sync problem.** The tricky part isn't reconciling state — it's deciding *when* to roll back gracefully so the user doesn't feel jolted.
- **CRDTs sound scarier than they are.** A few hundred lines of code handle the 90% case, and the ergonomic wins are immediate.
- **Build the failure modes first.** Disconnect handling, conflict resolution, stale tokens — all of it shaped the architecture more than the happy path did.

## What's next

I'd like to add offline-first support next — a service worker that queues mutations while disconnected and replays them on reconnect. The CRDT foundation should make this nearly free.
