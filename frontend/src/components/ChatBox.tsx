import { useState } from "react";
import axios from "axios";
import { ChatResponse } from "../types";

const ChatBox = () => {
  const [question, setQuestion] = useState<string>("");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const askBot = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post<ChatResponse>("http://localhost:8000/ask", { question });
      setResponse(res.data);
    } catch (err) {
      setResponse({
        answer: "Could not connect to the backend. Please try again.",
        article_number: "",
        article_title: "",
        source: "",
      });
    }

    setLoading(false);
  };

  return (
    <div className="bg-zinc-800 p-6 rounded-2xl shadow-lg space-y-6 text-white">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something about your constitutional rights..."
        className="w-full p-4 text-base rounded-xl bg-zinc-900 border border-zinc-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows={4}
      />
      <button
        onClick={askBot}
        disabled={loading}
        className="w-full py-3 text-lg font-semibold bg-blue-600 hover:bg-blue-700 rounded-xl transition duration-200 disabled:opacity-60"
      >
        {loading ? "Thinking..." : "Ask KYR Chatbot"}
      </button>

      {response && (
        <div className="bg-zinc-900 p-5 rounded-xl border border-zinc-700 space-y-4">
          <div>
            <h2 className="text-xl font-semibold text-blue-400 mb-2">KYR Chatbot says:</h2>
            <p className="leading-relaxed">{response.answer}</p>
          </div>

          {response.article_number && (
            <div className="text-sm text-zinc-400 mt-4">
              <p><strong>Article:</strong> {response.article_number} – {response.article_title}</p>
              <p className="italic text-zinc-500 mt-1">{response.source}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatBox;
