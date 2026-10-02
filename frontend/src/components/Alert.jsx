export default function Alert({ messages }) {
  const list = (Array.isArray(messages) ? messages : [messages]).filter(Boolean);
  if (list.length === 0) return null;
  return (
    <div className="alert alert-error" role="alert">
      {list.map((m, i) => <div key={i}>{m}</div>)}
    </div>
  );
}
