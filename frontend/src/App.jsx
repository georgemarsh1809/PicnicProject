import URLCodes from '../../backend/urlCodes.json';
import React, { useState } from 'react';

function App() {
    const [newUrl, setNewUrl] = useState('');

    // Standard state update when input value changes
    const handleInputChange = (e) => {
        setNewUrl(e.target.value);
    };

    // Handles keydown for 'Enter', so it can be used to submit
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleAddURL();
        }
    };

    // API Call and error handling for POST `/shorten`
    const handleAddURL = async () => {
        try {
            const res = await fetch('http://localhost:8000/shorten/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: newUrl,
                }),
            });

            if (!res.ok) {
                const error = await res.json();
                throw new Error(error.error);
            }
        } catch (error) {
            console.error('Error adding URL:', error);
            alert(error); // Show error message to user
        }

        // Resets the input to empty after a new URL addition is attempted
        setNewUrl('');
    };

    // API Call and error handling for GET `/{code}`
    const handleRedirect = async (code) => {
        try {
            const res = await fetch(`http://localhost:8000/${code}`, {
                method: 'GET',
            });

            if (res.status !== 302) {
                throw new Error('Failed to redirect');
            }

            const data = await res.json();
            window.open(data.longUrl, '_blank'); // Redirect to the long URL
        } catch (error) {
            console.error('Error redirecting:', error);
        }
    };

    return (
        <>
            <div className="header">
                <h1>Picnic Project</h1>
                <h2>
                    Welcome to my Picnic Project! This is a URL shortener API.
                </h2>
            </div>
            <div className="input-container">
                <input
                    placeholder="Enter a long URL you wish to shorten..."
                    className="url-input"
                    onChange={handleInputChange}
                    onKeyDown={handleKeyPress}
                    value={newUrl}
                />
                <button
                    className="add-button"
                    onClick={handleAddURL}
                    disabled={!newUrl}
                >
                    +
                </button>
            </div>
            <div>
                <h3>Saved URLs</h3>
                <table className="url-codes-table">
                    <thead>
                        <tr>
                            <th className="cell id-column">ID</th>
                            <th className="cell origin-column">Origin URL</th>
                            <th className="cell shorturl-column">
                                Shortened URL
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {URLCodes && URLCodes.length
                            ? URLCodes.map((codeObject, index) => {
                                  return (
                                      <tr key={`code-${index}`}>
                                          <td className="cell id-cell">
                                              {codeObject.id}
                                          </td>
                                          <td className="cell origin-cell">
                                              <a
                                                  href={codeObject.longUrl}
                                                  target="_blank"
                                              >
                                                  {codeObject.longUrl}
                                              </a>
                                          </td>
                                          <td className="cell">
                                              <button
                                                  className="redirect-button"
                                                  onClick={() =>
                                                      handleRedirect(
                                                          codeObject.code
                                                      )
                                                  }
                                              >
                                                  {codeObject.shortUrl}
                                              </button>
                                          </td>
                                      </tr>
                                  );
                              })
                            : 'No codes yet...'}
                    </tbody>
                </table>
            </div>
        </>
    );
}

export default App;
