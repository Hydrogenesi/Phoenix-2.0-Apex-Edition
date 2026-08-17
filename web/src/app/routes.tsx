import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import { CockpitPage } from "../pages/CockpitPage";
import { GraphPage } from "../pages/GraphPage";
import { FluxPage } from "../pages/FluxPage";
import { HomePage } from "../pages/HomePage";
import { Plate71Page } from "../pages/Plate71Page";

/**
 * Route table for the PhoenixEngine web app.
 *
 * /             → HomePage       (links to all views)
 * /cockpit      → CockpitPage    (full cockpit: graph + flux + plate71)
 * /graph        → GraphPage      (standalone graph layout view)
 * /flux         → FluxPage       (standalone flux renderer)
 * /plate71      → Plate71Page    (standalone Plate71 SVG viewer)
 */
export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true,          element: <HomePage /> },
      { path: "cockpit",      element: <CockpitPage /> },
      { path: "graph",        element: <GraphPage /> },
      { path: "flux",         element: <FluxPage /> },
      { path: "plate71",      element: <Plate71Page /> },
    ],
  },
]);
