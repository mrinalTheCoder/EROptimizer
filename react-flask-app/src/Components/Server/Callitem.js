import React from 'react';
import './CallItem.css'; 

const CallItem = ({ call, data, isActive, onClick }) => {

    const getTriageColor = (triage) => {
        switch(triage) {
            case 1: return 'red';
            case 2: return 'orange';
            case 3: return 'yellow';
            case 4: return 'lightgreen';
            case 5: return 'green';
            default: return 'grey';
        }
    };

    return (
        
        <div className="call-item">
            <div className="triage-dot" style={{ backgroundColor: getTriageColor(data.triage) }}></div>
            <p onClick={onClick}><strong>Call ID:</strong> {call.callid}</p>
            {isActive && (
                <div className="call-details">
                    {/* Add more details here */}
                    <p>{"Transcript: " + data.transcript}</p>
                    <p>{"Age: " + (data.age || "Unknown") }</p>
                    <p>{"Is Inpatient: " + (data.admit) }</p>
                    <p>{"Gender: " + (data.gender || "Unknown") }</p>
                    <p>{"Complaints: " + (data.complaints || []).join(", ") }</p>
                    <p>{"History: " + (data.history || []).join(", ") }</p>
                    <p>{"Triage: " + (data.triage || "Unknown") }</p>
                    <p>{"Meds: " + (data.meds || []).join(", ") }</p>
                </div>
            )}
        </div>
    );
};

export default CallItem;
