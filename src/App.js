import './App.css';
import React, { useState, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';

function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById('data').text);
  const [TempArtistlist, setTempArtistlist] = useState([]);
  const NameRef = useRef();
  const [Artistlist, setArtistlist] = useState(args.artistname_list);

  function AddArtist() {
    const TempArtistName = NameRef.current.value;
    if (TempArtistName === '') return;
    setTempArtistlist((prevTempArtistlist) => (
      [...prevTempArtistlist, { id: uuidv4(), name: TempArtistName }]
    ));
    NameRef.current.value = null;
  }

  function ClickToSave() {
    let TempArtistlists = [];
    TempArtistlist.forEach((temp) => {
      TempArtistlists = [...TempArtistlists, temp.name];
    });
    let Combinelist = [];
    if (Artistlist === undefined || Artistlist.length === 0) {
      Combinelist = [...TempArtistlists];
    } else {
      Combinelist = [...Artistlist, ...TempArtistlists];
    }

    console.log(JSON.stringify({ combinelist: Combinelist }));
    fetch('/artistsave', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ combineartistlist: Combinelist }),
    }).then((response) => response.json()).then((data) => {
      console.log(JSON.stringify(data));
      setArtistlist(data.finalartistlist);
      setTempArtistlist([]);
    });
  }

  function RemoveArtist(id) {
    const newTempArtistlist = [...TempArtistlist];
    const newtemp = newTempArtistlist.filter((newtempartist) => newtempartist.id !== id);
    setTempArtistlist(newtemp);
  }

  function RemoveArtistMain(name) {
    const newArtistname = Artistlist.filter((newartistname) => newartistname !== name);
    console.log(Artistlist);
    setArtistlist(newArtistname);
  }

  function ShowArtistList() {
    console.log(Artistlist);
    const list = Artistlist.map((showartistname) => (
      <div>
        <li style={{ color: 'blue' }} key={uuidv4()}>{showartistname}</li>
        <button type="button" onClick={() => RemoveArtistMain(showartistname)}>delete</button>
      </div>
    ));
    return (
      <ol>
        {list}
        <ShowList />
      </ol>
    );
  }

  function ShowList() {
    const list = TempArtistlist.map((showartistname) => (
      <div>
        <li style={{ color: 'red' }} key={showartistname.id}>{showartistname.name}</li>
        <button type="button" onClick={() => RemoveArtist(showartistname.id)}>delete</button>
      </div>
    ));
    return (
      <>
        {list}
      </>
    );
  }

  return (
    <>
      <div className="topbar">
        <nav className="container">
          <a href="profile" className="button">
            Profile
          </a>
          <a href="logout" className="button">
            Logout
          </a>
        </nav>
      </div>
      <div className="title">
        <h1>
          {args.username}
          &apos;s Favorite Artist&apos;s Top Tracks
        </h1>
      </div>
      {(args.nonecheck)
        ? (
          <div>
            <div>
              <div>
                <p1>Please save your favorite artist&apos;s ID below!</p1>
              </div>
              <>
                <div>
                  <input type="text" ref={NameRef} placeholder="Enter Name" />
                  <button type="button" onClick={AddArtist}>Add</button>
                  <button type="button" onClick={ClickToSave}>Save</button>
                </div>
              </>
              <div>
                <ol>
                  <ShowList />
                </ol>
              </div>
            </div>
          </div>
        )

        : (
          <>
            <div className="big-section">
              <div className="list">
                <p2>Your saved artists</p2>
                <nav>
                  <ol className="list-item">
                    <ShowArtistList />

                  </ol>
                </nav>
              </div>
              <div className="artist">
                <details>
                  <summary>
                    <p1 className="glow-on-hover">{args.artist_name}</p1>
                  </summary>
                  <div className="nav">
                    <div className="inner">
                      <p className="font-effect-fire-animation">{args.tracktitle}</p>
                      <a href={args.lyrics_url} target="_blank" rel="noreferrer">Lyrics</a>

                      <img alt="trackpic" src={args.trackpic} />

                      <audio controls src={args.songpreview}>
                        Your browser does not support the
                        <code>audio</code>
                        {' '}
                        element.
                        <track kind="captions" label="english_captions" />
                      </audio>
                    </div>
                  </div>
                </details>
              </div>
            </div>
            <div className="subtitle">
              <p1>Please save your favorite artist&apos;s ID below!</p1>
              <div>
                <input type="text" ref={NameRef} placeholder="Enter Name" />
                <button type="button" onClick={AddArtist}>Add</button>
                <button type="button" onClick={ClickToSave}>Save</button>
              </div>
            </div>
          </>
        )}
    </>
  );
}

export default App;
