// src/components/Sidebar.jsx
import { NavLink, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  Home as HomeIcon,
  BarChart2,
  ScatterChart,
  ChevronDown,
  ChevronRight,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/* central definition of every route shown in the sidebar             */
/* ------------------------------------------------------------------ */
const primaryRoutes = [
  { label: "Home", path: "/", icon: <HomeIcon className="w-4 h-4" /> },
  {
    label: "Exploratory Data Analysis",
    path: "/eda",
    icon: <BarChart2 className="w-4 h-4" />,
  },
  {
    label: "Visualizations",
    path: "/viz",
    icon: <ScatterChart className="w-4 h-4" />,
  },
];

const mlChildren = [
  { label: "ML Analysis 1", path: "/ml1" },
  { label: "ML Analysis 2", path: "/ml2" },
  { label: "ML Analysis 3", path: "/ml3" },
  { label: "ML Analysis 4", path: "/ml4" },
];

/* ------------------------------------------------------------------ */

export default function Sidebar() {
  const { pathname } = useLocation();
  const [openML, setOpenML] = useState(false);

  /* Auto-expand the ML group if any of its children is active */
  useEffect(() => {
    if (mlChildren.some(({ path }) => pathname.startsWith(path))) {
      setOpenML(true);
    }
  }, [pathname]);

  return (
    <aside className="flex flex-col w-64 h-screen bg-slate-100 border-r">
      {/* Logo / header */}
      <div className="px-6 py-5 text-3xl font-extrabold tracking-wide">
        <span className="text-teal-600">Progno</span>
        <span className="text-pink-600">six</span>
      </div>

      {/* Primary links */}
      <nav className="flex-1 px-3 space-y-1">
        {primaryRoutes.map(({ label, path, icon }) => (
          <SidebarLink key={path} to={path} icon={icon} label={label} />
        ))}

        {/* ML collapsible group */}
        <button
          onClick={() => setOpenML(!openML)}
          className={`flex w-full items-center justify-between px-3 py-2 rounded-md
                      font-medium transition-colors
                      ${
                        openML
                          ? "bg-teal-600 text-white"
                          : "text-slate-700 hover:bg-slate-200"
                      }`}
        >
          <span className="flex items-center gap-2">
            <ScatterChart className="w-4 h-4" />
            ML Analysis
          </span>
          {openML ? (
            <ChevronDown className="w-4 h-4" />
          ) : (
            <ChevronRight className="w-4 h-4" />
          )}
        </button>

        {openML && (
          <ul className="mt-1 space-y-0">
            {mlChildren.map(({ label, path }) => (
              <li key={path} className="ml-6">
                <SidebarLink size="sm" to={path} label={label} />
              </li>
            ))}
          </ul>
        )}
      </nav>
    </aside>
  );
}

/* ------------ small helper component so we don’t repeat Tailwind  --- */

function SidebarLink({ to, label, icon, size = "base" }) {
  return (
    <NavLink
      to={to}
      end
      className={({ isActive }) =>
        [
          "flex items-center gap-2 rounded-md px-3 py-2 transition-colors",
          size === "sm" ? "text-sm" : "font-medium",
          isActive
            ? "bg-teal-600 text-white"
            : "text-slate-700 hover:bg-slate-200",
        ].join(" ")
      }
    >
      {icon}
      {label}
    </NavLink>
  );
}
