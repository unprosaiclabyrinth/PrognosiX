import { useEffect, useRef, useState } from "react";

export default function PersistentIframe({ src, title, visible }) {
  const iframeRef = useRef(null);
  const [loaded, setLoaded] = useState(false);

  // set loaded flag the first (and only) time the iframe fires "load"
  useEffect(() => {
    const el = iframeRef.current;
    if (el) el.addEventListener("load", () => setLoaded(true), { once: true });
  }, []);

  return (
    <div
      className={`w-full h-screen ${visible ? "" : "invisible absolute -z-10"}`}
    >
      {!loaded && visible && (
        <div className="p-6 text-slate-500">Loading {title}…</div>
      )}

      {/* the iframe is mounted ONCE and kept; just toggled off-screen */}
      <iframe
        ref={iframeRef}
        src={src}
        title={title}
        className="w-full h-full border-0"
      />
    </div>
  );
}
