import React, { useState, useEffect } from "react";
import CallItem from "./Callitem";
import MapItem from "./MapItem";
import "./ServerSideComponent.css";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import "./ServerSideComponent.css";

const ServerComponent = () => {
  const [calls, setCalls] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeCallerID, setActiveCallerID] = useState(null);

  const fetchCalls = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/list_transcripts",
      );
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setCalls(data);
    } catch (error) {
      console.error("Fetch error:", error);
    }
    setIsLoading(false);
  };

  const toggleCallDetails = (callerID) => {
    setActiveCallerID(activeCallerID === callerID ? null : callerID);
  };

  useEffect(() => {
    fetchCalls();
    const interval = setInterval(fetchCalls, 5000); // Fetch every 5 seconds
    return () => clearInterval(interval); // Clean up
  }, []);

  // TODO: add logo src in line 43
  return (
    <div>
      <AppBar position="static">
      <Toolbar style={{ backgroundColor: "#3d405b" }}>
          {/* <img src={"/secondary.png"} alt="Logo" style={{ marginRight: 10, height: 50 }} /> */}
          <Typography variant="h6" style={{ flexGrow: 1, textAlign: "center" }}>
            <span style={{ color: 'white', fontSize: '40px' }}>[</span>
            <span style={{ color: 'white', fontWeight: 'bold', fontSize: '40px' }}>CALL.</span>
            <span style={{ color: 'red', fontWeight: 'bold', fontSize: '40px' }}>ER </span>
            <span style={{ color: 'white', fontSize: '40px' }}>]</span>
          </Typography>
        </Toolbar>
      </AppBar>
      <div className="server-side-container">
        <div className="calls-list">
          {isLoading ? (
            <p>Loading calls...</p>
          ) : calls.length > 0 ? (
            calls.map((call, index) => (
              <CallItem
                key={index}
                call={call}
                data={call.data}
                isActive={activeCallerID === call.callid}
                onClick={() => toggleCallDetails(call.callid)}
              />
            ))
          ) : (
            <p>No calls yet</p>
          )}
        </div>
        <div className="map-container">
          <MapItem />
        </div>
      </div>
    </div>
  );
};

export default ServerComponent;