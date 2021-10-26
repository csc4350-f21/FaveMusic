import logo from './logo.svg';
import './App.css';
import { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

// const LOCAL_STORAGE_KEY = 'temp_artistlist'
// const LOCAL_STORAGE_KEY2 = 'artistlist'

function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById("data").text);
  const [temp_artistlist, settemp_artistlist] = useState([]);
  const NameRef = useRef();
  // const artistname = ["Ariana", "Taylor"];
  const [artistlist, setartistlist] = useState(args.artistname_list);
  // const someValue = useRef(artistname)

  // useEffect(() => {
  //   const storedNames = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY2))
  //   if (storedNames) setartistlist(storedNames)
  // }, []);


  // useEffect(() => {
  //   localStorage.setItem(LOCAL_STORAGE_KEY2, JSON.stringify(artistlist))
  // }, [artistlist])

  // useEffect(() => {
  //   const storedNames = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY))
  //   if (storedNames) settemp_artistlist(storedNames)
  // }, []);


  // useEffect(() => {
  //   localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(temp_artistlist))
  // }, [temp_artistlist])

  function AddArtist(e) {
    const TempArtistName = NameRef.current.value;
    if (TempArtistName === '') return
    settemp_artistlist(prevtemp_artistlist => { return [...prevtemp_artistlist, { id: uuidv4(), name: TempArtistName }] });
    NameRef.current.value = null;

  }
  function ClickToSave() {
    let temp_artistlists = []
    temp_artistlist.forEach(temp => {
      temp_artistlists = [...temp_artistlists, temp.name]
    });
    const combinelist = [...artistlist, ...temp_artistlists];

    console.log(JSON.stringify({ "combinelist": combinelist }));
    fetch('/artistsave', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "combineartistlist": combinelist }),
    }).then(response => response.json()).then(data => {
      console.log(JSON.stringify(data))
      setartistlist(data.finalartistlist);
      settemp_artistlist([]);
    });
  }

  function RemoveArtist(id) {
    const newtemp_artistlist = [...temp_artistlist];
    const newtemp = newtemp_artistlist.filter(newtemp => newtemp.id !== id);
    settemp_artistlist(newtemp);
  }

  function RemoveArtistMain(name) {
    const newartistname = artistlist.filter(newartistname => newartistname !== name);
    console.log(artistlist)
    setartistlist(newartistname);

  }

  function ShowArtistList() {


    console.log(artistlist)

    const list = artistlist.map((showartistname) => {
      return (<div>
        <li style={{ color: 'blue' }} key={uuidv4()}>{showartistname}</li>
        <button onClick={() => RemoveArtistMain(showartistname)}>x</button>

      </div>)
    }
    )
    // const list = someValue.current.map((showartistname) => {
    //   return (<div>
    //     <li key={uuidv4()}>{showartistname}</li>
    //     <button onClick={() => remove_artistmain(showartistname)}>x</button>

    //   </div>)
    // }
    // )
    return (<ol>{list} <ShowList /></ol>)
  }

  function ShowList() {

    const list = temp_artistlist.map((showartistname) => {
      return (<div>
        <li style={{ color: 'red' }} key={showartistname.id}>{showartistname.name}</li>
        <button onClick={() => RemoveArtist(showartistname.id)}>x</button>
      </div>)
    }
    )
    return (<>{list}</>)
  }


  return (
    <>
      <div class="topbar">
        <nav class="container">
          <a href={'profile'} class="button">
            Profile
          </a>
          <a href={'logout'} class="button">
            Logout
          </a>
        </nav>
      </div>
      <div class="title">
        <h1>{args.username}'s Favorite Artist's Top Tracks</h1>
      </div>

      {(args.nonecheck) ?
        <>
          <div>
            <p1>Please save your favorite artist's ID below!</p1>
          </div>

          <form method="POST" action="/musicadd">
            <div>
              <input type="text" name="get_name" placeholder="Enter Name" autofocus="" />
              <button>Search n Save</button>
            </div>
          </form>
        </>

        :

        <>
          <div class="big-section">
            <div class="list">
              <p2>Your saved artists</p2>
              <nav>
                <ol class="list-item">

                  {/* {args.artistname_list.map((name, index) => {
                    return (
                      <form method="POST" action="/musicdelete">
                        <div>
                          <li key={index}>{name}
                            <button class="remove-button" name="delete_name" value={name}>x</button>
                          </li>
                        </div>
                      </form>
                    )
                  })} */}
                  <ShowArtistList />

                </ol>

                {/* <div>
                  <ol class="list-item">

                    {temp_artistlist.map((artistname) => {
                      return (
                        <div>
                          <li key={artistname.id}>{artistname.name}</li>
                          <button class="remove-button" onClick={() => remove_artist(artistname.id)}>x</button>
                        </div>
                      )
                    })}

                  </ol>
                </div> */}

              </nav>
            </div>
            <div class="artist">
              <details>
                <summary>
                  <p1 class="glow-on-hover">{args.artist_name}</p1>
                </summary>
                <div class="nav">
                  <div class="inner">
                    <p class="font-effect-fire-animation">{args.tracktitle}</p>
                    <a href={args.lyrics_url} target="_blank">Lyrics</a>

                    <img src={args.trackpic} />

                    <audio controls src={args.songpreview}>
                      Your browser does not support the
                      <code>audio</code> element.
                    </audio>
                  </div>
                </div>
              </details>
            </div>
          </div>
          <div class="subtitle">
            <p1>Please save your favorite artist's ID below!</p1>

            <form method="POST" action="/musicadd">
              <div>
                <input type="text" name="get_name" placeholder="Enter Name" autofocus="" />
                <button>Search n Save</button>
              </div>
            </form>
            <form method="POST" action="/musicdelete">
              <div>
                <input type="text" name="delete_name" placeholder="Enter name to remove" autofocus="" />
                <button>Remove</button>
              </div>
            </form>


            <label>
              <div>
                <input type="text" ref={NameRef} placeholder="Enter Name" />
                <button onClick={AddArtist}>Add</button>
                <button onClick={ClickToSave}>Save</button>
              </div>
            </label>
          </div>
        </>
      }
    </>
  );
}

export default App;
