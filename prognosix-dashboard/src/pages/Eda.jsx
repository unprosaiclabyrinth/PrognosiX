import React, { useState, useEffect } from "react";

/** Simple wrapper that iframes the Voilà page
 *  – shows a tiny loader the first time it mounts
 */
export default function Eda() {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const el = document.getElementById("eda-iframe");
    if (el) el.addEventListener("load", () => setLoaded(true), { once: true });
  }, []);

  return (
    <div className="w-full h-screen bg-white">
      {!loaded && (
        <div className="p-6 text-slate-500">Loading EDA notebook…</div>
      )}

      {/* Change localhost:8866 to your production URL later */}
      <iframe
        id="eda-iframe"
        src="http://localhost:8866/voila/render/eda.ipynb?"
        title="EDA Notebook"
        className="w-full h-full border-0"
      />
    </div>
  );
}
