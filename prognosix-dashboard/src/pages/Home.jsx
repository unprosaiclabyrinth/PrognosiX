import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    // TODO: hook this up to your backend / model / REST call
    console.log("User query:", query);
  }

  return (
    <section className="max-w-2xl mx-auto mt-24 px-6">
      <h1 className="text-3xl font-bold mb-6 text-slate-800">
        Welcome to PrognosiX
      </h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label
          htmlFor="user-input"
          className="text-sm font-medium text-slate-600"
        >
          Enter your question or patient details
        </label>

        <input
          id="user-input"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Predict CKD risk for a patient with …"
          className="w-full rounded-lg border border-slate-300 px-4 py-3
                     shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
        />

        <button
          type="submit"
          className="self-start rounded-lg bg-teal-600 px-6 py-2
                     font-medium text-white transition hover:bg-teal-700"
        >
          Submit
        </button>
      </form>
    </section>
  );
}
