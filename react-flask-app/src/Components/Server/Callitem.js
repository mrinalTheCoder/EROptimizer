import React from 'react';

const CallItem = ({ call, data, isActive, onClick }) => {
    return (
        <div className="call-item">
            <p onClick={onClick}><strong>Call ID:</strong> {call.callid}</p>
            {isActive && (
                <div className="call-details">
                    {/* Add more details here */}
                    <p>{"Transcript: " + data.transcript}</p>
                    <p>{"Age: " + (data.age || "Unknown") }</p>
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
