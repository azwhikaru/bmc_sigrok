# bmc_sigrok
Biphase Mark Coding (BMC) decoder script for libsigrok

Noticed that sigrok lacks support for the `Biphase encoding family` and created this script

Since I'm using it for USB PD Messaging, it references the decoder `usb_power_delivery`'s parameter. If you have other uses, you may need to modify the bitrate.

Doesn't recognize if Biphase Mark Coding is appeared, just stupidly converts levels. Doesn't look as clear as Saleae Logic's `Manchester` analyzer.

Works well in PulseView and DSView

USB PD Preamble's conversion preview. Starts with 0 and ends with 1. It just works, that's all.

![image](https://github.com/user-attachments/assets/bfbd0f06-d172-4dca-8c61-7cef2e3dd5b5)
