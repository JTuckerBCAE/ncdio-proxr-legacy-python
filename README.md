# NCD-IO ProXR Legacy Relay Controller PyLib

## What This Library is For

This python library can be used to control NCD-IO ProXR boards and connected Relay Expansion boards.
Supported devices can be found at [docs/ProXR.pdf Page 2](./docs/ProXR.pdf#page=2)

## About This Library

This library provides functions to setup and control ncd-io proxr.

### What This Library Does

- Allows multiple ways to control relays based on what works best for you and your application with no bit manipulation or direct byte writes
- On, off, and toggle commands.
- Control Relays by bank or index
- Timers and Flashers supported

### What This Library Doesn't Do

- This library does not create, maintain, or close any communication ports or sockets.
- These communication buses will be maintained by you in your application to allow you to keep it open or only open it as your applciation needs.
- This library does not release computer control for those series that have alternative automation capabilities such as Fusion and Taralist

## About the Code

### Instantiation

This library has class called Relay_Controller that can be instantiated by simply calling it and passing it a Communication Bus.
This bus should be a TCP/IP socket.

### Quirks

Older ProXR models may require that the user implement a form of rate limiting for commands. Commands sent in quick succession may get ignored by the controller.

Some socket configurations may experience drop outs due to TCP keep-alives being ignored by the controller.
