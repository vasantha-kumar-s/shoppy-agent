# Repository import observations

Source: https://github.com/vasantha-kumar-s/shoppy-agent, main at b52acaf.
This is an app source repository, not a deployed website. The website capture tool would copy GitHub's repository page rather than the requested app, so source files were imported directly.

Source live desktop/phone interaction checks are blocked: no hosted app or service URL supplied. Source code defines home, assistant, catalog, product details, cart, orders, and comparison pages. Home CTAs link to /assistant and /products. Sidebar contains all six main destinations. Catalog filters preserve query parameters. Assistant supports history visibility, voice replies, streaming chat, and microphone input. No source overlay, carousel, or video exists. Source mobile sidebar has no opening trigger; imported version supplies one. Services use a fixed demo user ID, retained without claiming user isolation.

All catalog, cart, orders, comparison results, conversation history, transcription, and agent responses require the external service. Their real-data checks remain blocked until its URL is supplied. No mock data or substitute AI was added. Source product imagery consists of category stock photos. The bundled hero.png is preserved, though the source home page does not display it.

## Preview checks
- Desktop 1280×1800: home, catalog, cart, orders, comparison, product detail, and assistant render. Home CTA reaches /assistant. History panel opens with its empty contents and closes. Sending a query reports the missing connection rather than fabricating an answer.
- Phone 390×844: home reaches its lower sections after wheel scrolling. Navigation opens, reaches /assistant, and closes. Assistant has no horizontal overflow. Screenshots: /tmp/browser/shoppy/desktop-home.png, desktop-bottom.png, desktop-sessions.png, desktop-disconnected.png, phone-home.png, phone-bottom.png, phone-assistant.png.
- Runtime page errors: none in the tested preview flow. Routing test passes. Preview build reports success.
- Live data, populated filters/comparison, checkout, conversation persistence, microphone transcription, and service audio remain blocked by the missing HTTPS service URL. Source/preview visual pairing remains blocked by the lack of a deployed source app.
- The seven original category photo URLs were downloaded and mapped to src/shoppy/assets/<category>.jpg.asset.json. These pointers replace the source hotlinks in product cards and product details.