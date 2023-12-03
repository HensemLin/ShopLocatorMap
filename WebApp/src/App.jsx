import { useState } from "react";
import Map from "./components/map";
import Navbar from "./components/navbar";

function App() {
  return (
    <div className="flex h-screen w-screen bg-white">
      <Navbar />
      <Map />
    </div>
  );
}

export default App;
