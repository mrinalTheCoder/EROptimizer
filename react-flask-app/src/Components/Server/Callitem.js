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
                </div>
            )}
        </div>
    );
};

export default CallItem;
