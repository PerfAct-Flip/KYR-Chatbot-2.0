import ChatBox from "./components/ChatBox";

const App = () => {
  return (
    <div className="min-h-screen bg-zinc-900 text-white flex items-center justify-center p-4">
      <div className="w-full max-w-3xl">
        <h1 className="text-3xl font-bold mb-6 text-center">
          🧾 Constitutional Rights Chatbot
        </h1>
        <ChatBox />
      </div>
    </div>
  );
};

export default App;
