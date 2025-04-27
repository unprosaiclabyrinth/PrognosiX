// src/App.jsx
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import PersistentIframe from "./components/PersistentIframe";
import Home from "./pages/Home";

/* ------------------------------------------------------------------ */
/*  ONE canonical list of notebook tabs                               */
/* ------------------------------------------------------------------ */
const notebooks = [
  {
    label: "Exploratory Data Analysis",
    path: "/eda",
    src: "http://localhost:8866/voila/render/eda.ipynb?",
  },
  {
    label: "Visualizations",
    path: "/viz",
    src: "http://localhost:8866/voila/render/Vis.ipynb",
  },
  {
    label: "ML Analysis 1",
    path: "/ml1",
    src: "http://localhost:8866/voila/render/ML1.ipynb",
  },
  {
    label: "ML Analysis 2",
    path: "/ml2",
    src: "http://localhost:8866/voila/render/ML2.ipynb",
  },
  {
    label: "ML Analysis 3",
    path: "/ml3",
    src: "http://localhost:8866/voila/render/ML3.ipynb",
  },
  {
    label: "ML Analysis 4",
    path: "/ml4",
    src: "http://localhost:8866/voila/render/ML4.ipynb",
  },
];

/* ------------------------------------------------------------------ */
/*  Layout that stays mounted; flips visibility of iframes            */
/* ------------------------------------------------------------------ */
function Layout() {
  const { pathname } = useLocation();

  return (
    <div className="flex">
      {/* Sidebar receives the same list for its menu */}
      <Sidebar notebooks={notebooks} />

      <main className="flex-1 min-h-screen bg-white">
        {notebooks.map((n) => (
          <PersistentIframe
            key={n.path}
            src={n.src}
            title={n.label}
            visible={pathname === n.path}
          />
        ))}

        {pathname === "/" && <Home />}
      </main>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Top-level router                                                  */
/* ------------------------------------------------------------------ */
export default function App() {
  return (
    <BrowserRouter>
      {/* Wildcard means Layout handles every route */}
      <Routes>
        <Route path="/*" element={<Layout />} />
      </Routes>
    </BrowserRouter>
  );
}
