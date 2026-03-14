# Build Verification Report

Date: 2026-03-15

## Hydration

- ECC hydrated from pinned commit `32e9c293f0d6f04e3b9bf804887747d5c8b5dc10`.
- Skillful hydrated from pinned commit `9ee443f5d61f1783cdbf6e01acb3a587b3c3b4f8`.
- Both source trees are present in:
  - `everything-claude-code`
  - `opencode-skillful`

## Validation Commands Run

### ECC

1) Install deps

```bash
npm ci
```

Result:

- success
- note: npm audit reported 6 vulnerabilities (2 moderate, 4 high)

2) Run full test/validator suite

```bash
npm test
```

Result:

- success
- validators passed (agents, commands, rules, skills, hooks)
- final test summary:
  - total: 992
  - passed: 992
  - failed: 0

### OpenCode Skillful

1) Install deps (Yarn)

```bash
corepack yarn install
```

Result:

- success
- lockfile generated: `yarn.lock`

2) Run tests (Yarn + Vitest)

```bash
corepack yarn vitest run --config vitest.config.ts
```

Result:

- success
- final test summary:
  - test files: 11 passed
  - tests: 211 passed
  - failed: 0

3) Type check

```bash
corepack yarn tsc --noEmit
```

Result:

- success

4) Build bundle + declarations

```bash
rm -rf dist
corepack yarn esbuild ./src/index.ts --bundle --platform=node --format=esm --target=node20 --outfile=dist/index.js
corepack yarn tsc --project tsconfig.build.json
```

Result:

- success
- outputs:
  - `dist/index.js`
  - declaration files in `dist/`

## Outcome

- Hydration: complete
- Overlay artifacts: complete
- ECC verification: complete and passing
- Skillful verification: complete and passing on Yarn toolchain

## Recommended Follow-Up

Run these for local verification:

```bash
cd opencode-skillful
corepack yarn install
corepack yarn vitest run --config vitest.config.ts
corepack yarn tsc --noEmit
corepack yarn esbuild ./src/index.ts --bundle --platform=node --format=esm --target=node20 --outfile=dist/index.js
corepack yarn tsc --project tsconfig.build.json
```
