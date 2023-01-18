# Wii U Websocket

**Proof-of-concept Wii&nbsp;U Gamepad touchscreen&nbsp;→&nbsp;PC mouse cursor interface**

---

So, there's a little program called [UsendMii](https://wiiubrew.org/wiki/UsendMii) - it promises to let you use your Wii U Gamepad as a PC controller. And to give it some credit, for [some](https://media.24ways.org/2012/debenham/diagramxl.png) button inputs, it works really well, the latency is unnoticeable to me. But wanting to mess around with DS and 3DS emulators, I really wanted to use the Gamepad to get the true "resistive touchscreen" feeling[^1] that's hard to come by nowadays. [And I'm not the only one!](https://www.reddit.com/r/Citra/comments/cj6zca/wii_u_gamepad_as_touchscreen/)

The program teases this function pretty well: you're given a live preview of the touchscreen input, but as it turns out, all you can do with it is map rectangular zones to simulated keyboard presses, similar to when you're running an emulator on your phone. The general concept for the program is great! But this tiny little detail gets so close, but not quite there, and it ruins the whole thing.

So I made my own.

[^1]: Of course, I acknowledge that it would've been much easier to use a laptop/phone touchscreen (these are capacitive), or maybe even a graphic tablet if you're feeling fancy, but *this* is much jankier and much cooler.

For those out of the loop, here's what's happening:

- There's a local Websocket server for sending messages between devices
- The **Wii U browser** loads a webpage from our HTTP server
- We weild the stylus and do stuff on the Gamepad
- A script on that page sends messages to the Websocket server
- Meanwhile, a Python script reads them and **controls the PC's mouse**

And yeah, it all works **without** having to hack your Wii U! <sub>(though don't quote me on that, since I don't really have an unhacked Wii U to try this out on.)</sub>

## Sounds cool, can I see this in action?

Sure! Here's a demo with me "drawing" in Paint.NET: [(also on YouTube)](https://youtu.be/3ugmqohBFCM)

https://user-images.githubusercontent.com/3956863/213112444-029c8c27-3c75-4e3d-8d19-41bc8d04a9e6.mp4

Of course, this works with anything on your PC, since it just simulates mouse movements. Feel free to use it with Citra, CEMU or any of your other touch-screen needs.

## I wanna try running it myself! How do I set this up?

> **Warning**
> Again, this is a proof of concept. I spent like 2 hours total on this thing and it's not polished or probably bug-free at all. Writing this readme took me more time than actually making the rest.

### Prerequisites

[Node.js](https://nodejs.org/en/download/releases/) for the Web&shy;socket server[^2] and [Python 3](https://www.python.org/downloads/) for moving your mouse.

<sup>(I tried doing this with AutoHotkey instead of Python at first, but it was more painful than I was willing to endure.)</sup>

I'm not too sure if you need these *specific* versions, but it's what I have and it works for me.

```
> node --version
v16.13.1

> python --version
Python 3.10.6
```

> **Note** 
> I only tested this on Windows 10 x64, so I can't guarantee that the program (or the commands used to install it) are going to work or any other systems.

You also need to have your Wii U and PC running on the same network. ... Hey, since you're already going to the internet settings, why not [change the DNS](https://wiiu.hacks.guide/#/block-updates?id=dns-blocking) to block Nintendo updates?

[^2]: Feel free to use your own thing for the Websocket stuff, all this does is repeat (or "echo") every received message to all connected clients.

### Components

Here's the most important parts and what they do:

<dl>
  <dt><code>index.js</code></dt>
  <dd>The Websocket server, <em>hardcoded to port 8080</em>. <a href="https://github.com/Matojeje/Wii-U-Websocket/blob/main/index.js#L26">Tweak as needed.</a></dd>
  <dt><code>wiiu.html</code></dt>
  <dd>The "sender client" that you <a href="#4-open-the-wii-u-browser">load up on the Wii U</a>, again with <a href="https://github.com/Matojeje/Wii-U-Websocket/blob/main/wiiu.html#L16">hardcoded things you have to edit.</a></dd>
  <dt><code>mousey.py</code></dt>
  <dd>The "receiver client" that does the mouse moving stuff, with more <a href="https://github.com/Matojeje/Wii-U-Websocket/blob/main/mousey.py#L13">hardcoded things</a>.<br>I named it this way to stop Python complaining about "circular dependencies".</dd>
</dl>

### Installation

> **Note**
> Do each step its own separate terminal / command prompt.

#### 1. Set up the Websocket server

```
npm install express http ws
node .
```

#### 2. Run the Python script

```
pip install mouse
python mousey.py
```

#### 3. Figure out your local IP address (Windows)

```ps
ipconfig /all | findstr "IPv4"
```
> **Warning**
> Change the code in [`wiiu.html` (line 16)](https://github.com/Matojeje/Wii-U-Websocket/blob/main/wiiu.html#L16) to point to your PC.

If the above command shows several different addresses, drop the filter part and just `ipconfig /all` and look for the right network adapter name.

#### 4. Open the Wii U Browser

Navigate to the place where you're hosting your edited `wiiu.html`, making sure not to forget to *specifically* write the `http://` too. (`https` where applicable) – When I entered my IP *without* the protocol, I got redirected to a search engine.

> **Note**
> The web server is **not** included, use your favorite solution for serving static html files![^3]

[^3]: My go-to is the (now-obsolete) Live Server extension for VS Code, though Caddy server might also work. Since what I used is an *extension*, there's no easy way for me to include it here, and adding a specific HTML server to the Express stuff in `index.js` would've taken too much effort. Sorry!

#### 5. Double-check the Websocket connection

Your Wii U should now display a mostly-blank page with two checkboxes on it, and if you look at the Node.js terminal that's got `index.js` running on it, you should hopefully see that both Python and Wii U connected to it successfully:

```
Server started on port 8080
Client connected
Client connected
```

> If not, **please make sure that you didn't forget to change any of the hard-coded IP addresses and ports** to something more suitable for you!

<details>
<summary>
<h4>6. Lament the defunct pen-trail feature</h4>
</summary>
Sure enough, I wanted to make it easier to draw with this thing, so I added a canvas to the Wii U's side of things, where a temporary trail would follow your stylus, letting you orientate yourself in your scribbles before they slowly faded out.
  
![Scribble that fades out](https://user-images.githubusercontent.com/3956863/213115137-89e31081-4e08-49d0-ac16-d25a7fb606a4.png)

Unfortunately, the Wii U doesn't quite handle the browser mouse events like expected. But if you [open the html file](https://rawcdn.githack.com/Matojeje/Wii-U-Websocket/e661eafdb1889a121b6712771639f49ce6aa7159/wiiu.html) in your PC browser of choice, and (hold)&shy;drag your mouse on the canvas <sub>(in the upper left, remember – it's the 480p gamepad resolution)</sub>, it works well!
</details>

<details>
<summary>
<h4>7. Realize you would've been better off using a <abbr title="Dualshock 4 (Sony Playstation)">DS4</abbr> controller</h4>
</summary>
That's right! It has both a touchscreen and motion controls, and as a big plus, it's an actual usable controller.
</details>

### Usage / Options

You can find two checkboxes on the Wii U page:

- [ ] **Drag mouse**

Enable this to simulate pressing the left mouse button. **Off** by default, so drawing on the Gamepad screen just moves your stylus, but doesn't click anything.

- [x] **Smooth mouse**

Poor attempt at mouse stabilization. It's based on functionality in `mouse` [(the Python package)](https://github.com/boppreh/mouse#mousemovex-y-absolutetrue-duration0-steps_per_second1200), and is **on** by default, but tweak the `duration` yourself in `mousey.py` for best results.

Please note that – while a smart idea – using external stabilization programs like [SilkyShark](https://github.com/stoicshark/silkyshark) doesn't work, as the two programs end up fighting for control over the mouse, and you might end up with something undesirable that looks like the Beziers screensaver from Windows XP. <sub>Too lazy to boot up the Wii U again just to make a visual example.</sub> You might have better luck using built-in stabilizers in art programs like [FireAlpaca](https://firealpaca.com/), as those don't tend to directly affect your mouse!

> **Note**
> If you have trouble clicking the checkboxes, there's a bunch of ways to scale them up, like adjusting the font size with CSS, smaller `<meta ... viewport` width and height, or changing `user-scalable` to `yes` [here](https://github.com/Matojeje/Wii-U-Websocket/blob/main/wiiu.html#L5)! Watch out for double-click triggering zooming, though.

## FAQ (Frequently anticipated questions)

### Can I use this for CEMU?

I guess! I haven't tried it, but it *should* work! Don't forget to tick the Drag Mouse checkbox. Now here's my question: Why do you want to emulate a Wii U and use a real Wii U to control it?

### How do I get my PC screen to show up on the gamepad?

No idea. I've heard people mention libDRC a lot when it comes to this stuff. Other people mention something called Moonlight, which seems to be a way to trick Nvidia software to stream gameplay to your Gamepad as if it was a Shield.

### Why does the HTML look so awful and outdated?

I tried to play it extra safe to make sure it works on Wii U's 11 year old browser. Plus, I copied part of it from UsendMii where it was hiding deep inside `RCDATA\DATA_INDEXWIIU`.

### How can I draw better with this thing?

Use some Wii U software that's intended for drawing, like the Miiverse posting part of Splatoon. Oh wait--

### This sucks. I could've done better.

I agree! Also, not a question. This isn't meant to be a serious solution, thooouugh if you *do* wanna improve this [bodgy](https://www.youtube.com/watch?v=lIFE7h3m40U) mess, I'll be reading through [issues](https://github.com/Matojeje/Wii-U-Websocket/issues) and [<abbr title="pull requests">PR</abbr>s](https://github.com/Matojeje/Wii-U-Websocket/pulls) at least throughout 2023.

[Useful link:](https://web.archive.org/web/20180913011631/https://www.nintendo.com/wiiu/built-in-software/browser-specs) Official developer reference for the Wii U browser's extended Gamepad capabilities

Let's discuss on [Discord](https://discordid.netlify.app/?id=189400498497912832)!
