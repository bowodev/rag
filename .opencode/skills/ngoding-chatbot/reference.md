# Chatbot React reference

## Minimal chat state example

```tsx
type Msg = { id: string; role: "user" | "assistant"; content: string };

function ChatPanel({ botId }: { botId: string }) {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  // derived — do not store separately
  const canSend = input.trim().length > 0 && !isSending;

  async function handleSend() {
    if (!canSend) return;
    // optimistic user message + mutation/stream call
  }

  return (
    <>
      <MessageList messages={messages} />
      <Composer value={input} onChange={setInput} onSend={handleSend} disabled={!canSend} />
    </>
  );
}
```

## Streaming as an external system

```tsx
useEffect(() => {
  if (!streamUrl) return;
  const controller = new AbortController();
  startStream(streamUrl, {
    signal: controller.signal,
    onToken: (t) => setMessages(/* functional update */),
  });
  return () => controller.abort();
}, [streamUrl]);
```

Only use an Effect when synchronization with the stream/connection is required. User clicking Send belongs in an event handler that *starts* that external sync.

## Purity & hooks

- Follow Rules of Hooks; enable `eslint-plugin-react-hooks`
- Never mutate `messages` in place — always new arrays/objects
