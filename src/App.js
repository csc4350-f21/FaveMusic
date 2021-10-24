import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';



function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById("data").text);
  const [temp_artistlist, settemp_artistlist] = useState([]);

  function add_artist(name_input) {
    console.log(JSON.stringify({ 'temp': temp_artistlist }));
    console.log(name_input)
    settemp_artistlist(arr => [...arr, name_input])
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
        {temp_artistlist.map((name, index) => {
          return (
            <div>
              <li key={index}>{name}
              </li>
            </div>
          )
        })}
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

                  {args.artistname_list.map((name, index) => {
                    return (
                      <form method="POST" action="/musicdelete">
                        <div>
                          <li key={index}>{name}
                            <button class="remove-button" name="delete_name" value={name}>x</button>
                          </li>
                        </div>
                      </form>
                    )
                  })}

                </ol>
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

            {/* <form method="POST" action="/musicadd">
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
            </form> */}
            <form>
              <div>
                <input type="text" name="get_name" id="get_name" placeholder="Enter Name" autofocus="" />
                <input type="button" value="a" onClick={add_artist('b')}>Add</input>
              </div>
            </form>
          </div>
        </>
      }
    </>
  );
}

export default App;
