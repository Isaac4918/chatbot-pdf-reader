export default function ClearButton({ onClear }) {
  return (
    <div className="text-end p-3 mt-2">
      <button
        className="btn btn-sm btn-outline-light"
        onClick={onClear}
        title="Clear the conversation"
      >
        Clear Conversation
      </button>
    </div>
  );
}
