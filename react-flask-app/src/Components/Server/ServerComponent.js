import React, { useState, useEffect } from 'react';
import CallItem from './Callitem';
import MapItem from './MapItem';
import './ServerSideComponent.css'; 

const ServerComponent = () => {
    const [calls, setCalls] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [activeCallerID, setActiveCallerID] = useState(null);

    const fetchCalls = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/list_transcripts');
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            setCalls(data);
        } catch (error) {
            console.error('Fetch error:', error);
        }
        setIsLoading(false);
    };

    const toggleCallDetails = (callerID) => {
        setActiveCallerID(activeCallerID === callerID ? null : callerID);
    };

    useEffect(() => {
        fetchCalls();
        const interval = setInterval(fetchCalls, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
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
    );
};

export default ServerComponent;
