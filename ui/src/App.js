import React, { useState } from 'react';
import './App.css';
import validator from 'validator';
import {createLink} from "./service";

function App() {
  const [url, setUrl] = useState('');
  const [shortLink, setShortLink] = useState('');
  const [fetchFailed, setFetchFailed] = useState(false);
  const [urlValid, seturlValid] = useState(true);
  const [urlEmpty, setUrlEmpty] = useState(true);

  const handleSend = async () => {
    if (!urlValid || urlEmpty) {
        return;
    }

    try {
      setFetchFailed(false);
      setShortLink('');

      const response = await createLink(url);
      setShortLink(response.short_url);

    } catch (error) {
      setFetchFailed(true);
      console.log(error.details);
    }
  };

  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    setShortLink('');
    setUrl(inputValue);
    setUrlEmpty(inputValue === '');
    seturlValid(validator.isURL(inputValue, { require_protocol: true}) || urlEmpty);
  };

  return (
    <div className="App">
        <h1>URL Shortener</h1>
        <div className="input-container">
          <span>Enter URL:</span>
          <input
              type="url"
              value={url}
              onChange={handleInputChange}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Enter URL"
          />
          <button onClick={handleSend} disabled={urlEmpty || !urlValid}>Send</button>
        </div>
        {!urlValid && <span className="error">Invalid URL</span>}
        {shortLink && !fetchFailed && <span className="shortlink">Your short link: <a href={shortLink} target="_blank" rel="noreferrer">{shortLink}</a></span>}
        {fetchFailed && <span className="error">Oops, failed to create a link</span>}
    </div>
  );
}

export default App;