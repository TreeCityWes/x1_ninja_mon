# x1_ninja_mon

Monitor for new token launches on [X1](https://x1.ninja) / X1.Ninja.

## Brand color

The live X1.Ninja palette is documented in [`brand/`](brand/BRAND.md) so this monitor (and anything else in the family) can match the site instead of inventing a second look.

- Visual book: [brand/index.html](brand/index.html)
- Tokens: [brand/tokens.css](brand/tokens.css) · [brand/tokens.json](brand/tokens.json)

Core product accent is **X1 Cyan** `#00B8FF` on void black. Logo navy is identity-only.

## Run

Put your X1.Ninja API key in `.env` (see `.env.example`):

```
x1_api=x1_your_key_here
```

Then:

```
python3 server.py
```

Open [http://localhost:3000](http://localhost:3000). The page lists the newest XDEX pools and refreshes every 20 seconds. The key stays on the server.
