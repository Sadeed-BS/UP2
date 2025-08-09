import { useState, useEffect, useRef } from "react";
import { ArrowUpIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatMessage {
  content: string;
  type: "human" | "ai";
}

export const Demo = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);

  const bottomRef = useRef<HTMLDivElement | null>(null);
  const chatContainerRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll only if near bottom
  useEffect(() => {
    const container = chatContainerRef.current;
    if (!container) return;

    const isNearBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight < 50;

    if (isNearBottom) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatHistory]);

  const handleSendMessage = async () => {
    if (!message.trim()) return;
    setIsSending(true);

    const userMessage: ChatMessage = { content: message, type: "human" };
    const updatedHistory = [...chatHistory, userMessage];

    setChatHistory(updatedHistory);
    setMessage("");

    try {
      const response = await fetch("https://up-fmhw.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_message: message,
          chat_history: updatedHistory,
        }),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      setChatHistory((prev) => [...prev, { content: data.response, type: "ai" }]);
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      {/* Navbar */}
      <nav className="sticky top-0 z-10 bg-gray-900 border-b border-gray-700 shadow-sm">
        <div className="max-w-5xl mx-auto flex justify-between items-center p-4">
          <h1 className="text-xl font-bold tracking-wide">Aibohphobia AI</h1>
          <span className="text-gray-400 text-sm">Powered by AI</span>
        </div>
      </nav>

      {/* Chat messages */}
      <main
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto px-4 py-6 max-w-5xl mx-auto w-full"
      >
        <div className="space-y-4">
          {chatHistory.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.type === "human" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`p-3 rounded-2xl max-w-[80%] md:max-w-[70%] break-words shadow ${
                  msg.type === "human"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-gray-300 text-gray-900 rounded-bl-none"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {/* AI typing indicator */}
          {isSending && (
            <div className="flex justify-start">
              <div className="p-3 rounded-2xl bg-gray-300 text-gray-900 rounded-bl-none animate-pulse max-w-[80%] md:max-w-[70%]">
                Typing...
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </main>

      {/* Input area */}
      <div className="border-t border-gray-700 bg-gray-900 px-4 py-3">
        <div className="flex gap-2 max-w-5xl mx-auto w-full">
          <Textarea
            className="flex-1 h-16 resize-none appearance-none border border-gray-600 bg-gray-800 text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <Button
            className="flex items-center justify-center bg-blue-600 hover:bg-blue-700 rounded-lg p-3"
            onClick={handleSendMessage}
            disabled={!message.trim() || isSending}
          >
            <ArrowUpIcon className="w-5 h-5 text-white" />
          </Button>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 border-t border-gray-700 text-gray-400 text-center py-4 text-sm">
        © {new Date().getFullYear()} Aibohphobia AI — All rights reserved.
      </footer>
    </div>
  );
};
