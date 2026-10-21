# Dashboard React reference

## State placement (Thinking in React)

- Store the minimal state (e.g. `selectedBotId`, upload form fields)
- Derive view models during render (`readySources = sources.filter(s => s.status === "ready")`)
- Lift state to the nearest common owner; pass setters/callbacks down

## Avoid unnecessary Effects

```tsx
// ❌ syncing derived state
useEffect(() => setCount(items.length), [items]);

// ✅ derive
const count = items.length;
```

```tsx
// ❌ fetch-in-effect when a query library exists
useEffect(() => { fetchSources().then(setSources); }, [botId]);

// ✅ query hook
const { data: sources } = useSourcesQuery(botId);
```

## Event handlers vs Effects

- Upload/delete/send-message → event handlers / mutations
- Effects only for external sync (e.g. attaching a non-React widget)

## Purity

- Do not mutate props/state
- Same props/state → same render output
- Enable Strict Mode + `eslint-plugin-react-hooks`
