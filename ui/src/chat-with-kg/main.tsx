import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.js";

import "@neo4j-ndl/base/lib/neo4j-ds-styles.css";
import "./index.css";

const container = document.getElementById("root");
const root = createRoot(container!);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
