document.addEventListener('DOMContentLoaded', function() {
    const allElts = document.querySelectorAll('.App__category-item');
    allElts.forEach(item => {
        item.addEventListener('click', function(event) {
            const selectedCategory = item.parentElement.getAttribute('data-category');
            console.log("Clicked:", selectedCategory);
            localStorage.setItem('selectedCategory', selectedCategory);
            allElts.forEach(item => {
                item.classList.remove('App__category-item--selected');
            });
            item.classList.add('App__category-item--selected');

            const href = item.parentElement.getAttribute('href');
            if (href && href !== "#" && href !== "") {
                window.location.href = href;
            }
        });
        const selectedCategory = localStorage.getItem('selectedCategory');
        if (selectedCategory) {
            const selectedElement = document.querySelector(`[data-category="${selectedCategory}"] .App__category-item`);
            if (selectedElement) {
                allElts.forEach(item => {
                    item.classList.remove('App__category-item--selected');
                });
                selectedElement.classList.add('App__category-item--selected');
            }
        }
    });

    const genreSelect = document.querySelector('#genreSelect');

    function setSelectedGenreOption() {
        const queryParams = new URLSearchParams(window.location.search);
        const selected = queryParams.get('genre_id');

        // if (genreSelect.options){
            for (const option of genreSelect.options) {
                if (option.value === selected) {
                    option.selected = true;
                    return;
                }
            }
        // }

    }
    if (genreSelect){
        setSelectedGenreOption();
    }

    if (genreSelect){
        // setSelectedGenreOption();
        genreSelect.addEventListener("change", function() {
            console.log("Filtering... ");
            const selectedGenre = genreSelect.options[genreSelect.selectedIndex];
            const selectedUrl = selectedGenre.getAttribute('data-url');
    
            if (selectedUrl){
                window.location.href = selectedUrl;
            }
        });
    }






    var countDownElt = document.getElementById('countdown');

    if (countDownElt) {
        var countdown = 300;
        var timer = setInterval(function() {
            countdown--;
            countDownElt.innerHTML = "Time remaining: " + countdown + " seconds";
            if (countdown <= 0) {
                clearInterval(timer);
                countDownElt.innerHTML = "OTP has expired";
            }
        }, 1000);
    }

    var menuToggle = document.getElementById('menu-toggle');
    var menuOptions = document.getElementById('menu-options');
    

    // var addSongsOption = document.getElementById('add-songs');
    // var deletePlaylistOption = document.getElementById('delete-playlist');


    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (menuOptions.style.display === 'none' || menuOptions.style.display === '') {
                menuOptions.style.display = 'block';
                menuToggle.style.opacity = '0.4'
            } else {
                menuOptions.style.display = 'none';
                menuToggle.style.opacity = '1'
            }
        });
    }
    if (menuOptions){
        document.addEventListener('click', function(e) {
            var target = e.target;
            if (target !== menuToggle && target !== menuOptions) {
                menuOptions.style.display = 'none';
            }
        });
    }

    var menuIcons = document.querySelectorAll('.menu__for-Song');
    if (menuIcons) {
        menuIcons.forEach((icon, index) => {
            icon.addEventListener('click', function(e) {
                console.log("Menu Clicked");
                e.stopPropagation();
                var menu = icon.parentElement.querySelector('.songMenu');
                menu.addEventListener("click", function(e) {
                    console.log("Option clicked!");
                    e.stopPropagation();
                });
                if (menu.style.display === 'none' || menu.style.display === '') {
                    menu.style.display = 'block';
                    menuIcons[index].style.opacity = '0.4';
                } else {
                    menu.style.display = 'none';
                    menuIcons[index].style.opacity = '1';
                }
            });
        });
    }


    const likeIcon = document.querySelector('.like-icon');
    

    if (likeIcon) {
        likeIcon.addEventListener("click", (e) => {
            e.preventDefault();
            const csrftoken = getCookie('csrftoken');
            const playlistId = parseInt(likeIcon.getAttribute('data-playlist-id'));
            const albumId = parseInt(likeIcon.getAttribute('data-album-id'));

            if (playlistId) {
                const data = {
                    'playlist_id': playlistId
                };
                $.ajax({
                    type: "POST",
                    headers: { "X-CSRFToken": csrftoken },
                    url: "/like-playlist/",
                    data: data,
                    dataType: 'json',
                    success: function(response) {
                        console.log(response);
                        const likeCountElement = document.querySelector('.playlist__likes-count');
                        if (likeCountElement) {
                            likeCountElement.innerText = response.likes_count + ' likes';
                        }
                        if (likeIcon.style.filter === "grayscale(100%)") {
                            likeIcon.style.filter = "grayscale(0%)"; // Remove grayscale
                        } else {
                            likeIcon.style.filter = "grayscale(100%)"; // Apply grayscale
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            } else {
                const data = {
                    'album_id': albumId
                };
                $.ajax({
                    type: "POST",
                    headers: { "X-CSRFToken": csrftoken },
                    url: "/like-album/",
                    data: data,
                    dataType: 'json',
                    success: function(response) {
                        console.log(response);
                        const likeCountElement = document.querySelector('.album__likes-count');
                        if (likeCountElement) {
                            likeCountElement.innerText = response.likes_count + ' likes';
                        }
                        if (likeIcon.style.filter === "grayscale(100%)") {
                            likeIcon.style.filter = "grayscale(0%)"; // Remove grayscale
                        } else {
                            likeIcon.style.filter = "grayscale(100%)"; // Apply grayscale
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }       
        });
    }

    const likeSongBtns = document.querySelectorAll('.fire__blackWhite');
    const functionLike = document.querySelector('.function-like');

    const likeHandler = function() {
        return function(event) {
            event.stopPropagation();
            theFire = event.target;
            song_id = theFire.getAttribute('data-song-id');

            const elementWithClickedClass = document.querySelector('.clicked');

            console.log('Fire Clicked..', song_id);

            const csrftoken = getCookie('csrftoken');
            $.ajax({
                type: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                url: '/like-song/' + `${song_id}`,
                data: {},
                dataType: 'json',
                success: function (response) {
                    console.log(response);
                    if (response.songLikedCount === 0) {
                        theFire.style.filter = 'grayscale(100%)';
                        if (elementWithClickedClass && elementWithClickedClass.getAttribute('data-song-id') === song_id) {
                            console.log('changing func')
                            functionLike.style.filter = 'grayscale(100%)';
                        } 
                    }
                    else {
                            theFire.style.filter = 'grayscale(0%)';
                            if (elementWithClickedClass && elementWithClickedClass.getAttribute('data-song-id') === song_id) {
                            functionLike.style.filter = 'grayscale(0%)';
                            }
                    }
                    },
                    error: function (xhr, errmsg, err) {
                        console.log(xhr.status + ': ' + xhr.responseText);
                    }
                });
        }
    }

    function likeHandlerZ(id) {
        // console.log(id, typeof(id));
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            url: '/isliked/',
            data: {'id': id},
            dataType: 'json',
            success: function (response) {
                console.log(response);
                if (response.Liked === 'false') {
                    functionLike.style.filter = 'grayscale(100%)';
                        console.log('changing function love icon from Z')
                }
                else {
                        functionLike.style.filter = 'grayscale(0%)';
                        console.log('changing function like icon from Z')
                }
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ': ' + xhr.responseText);
                }
            });
    }

    function likeHandlerX() {
        return function(event) {
            const elementWithClickedClass = document.querySelector('.clicked');
            const id = elementWithClickedClass.getAttribute('data-song-id');
            const fire = document.querySelector(`span[data-song-id="${id}"]`);
            const csrftoken = getCookie('csrftoken');

            $.ajax({
                type: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                url: '/like-song/' + `${id}`,
                data: {},
                dataType: 'json',
                success: function (response) {
                    console.log(response);
                    if (response.songLikedCount === 0) {
                        fire.style.filter = 'grayscale(100%)';
                            functionLike.style.filter = 'grayscale(100%)';
                    }
                    else {
                        fire.style.filter = 'grayscale(0%)';
                        functionLike.style.filter = 'grayscale(0%)';    
                    }
                },
                    error: function (xhr, errmsg, err) {
                        console.log(xhr.status + ': ' + xhr.responseText);
                    }
            });
        }
    }
    
    
    likeSongBtns.forEach((btn) => {
        btn.addEventListener("click", likeHandler());
    });

    functionLike.addEventListener("click", likeHandlerX());

    function deleteSong() {
        return function(event){
            id = event.target.getAttribute('data-song-id');
            const csrftoken = getCookie('csrftoken');
            $.ajax({
                type: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                url: `/delete-song/${id}`,
                dataType: 'json',
                success: function (data) {
                    console.log(data.message);
                    const deletedElement = document.querySelector(`[data-song-id="${id}"]`);
                    if (deletedElement) {
                        deletedElement.remove();
                    } else {
                        console.log('Element not found');
                    }
                    console.log('Updating song lists...')
                    const updatedSongs = document.querySelectorAll('.song');
                    songs = Array.from(updatedSongs);
                    // songs = document.querySelectorAll('.songs');
                    
                },
                error: function (xhr, errmsg, err) {
                    console.error(xhr.status + ': ' + xhr.responseText);
                }
            });
        }
    }

    const deleteBtn = document.querySelectorAll('.delete__Song');

    deleteBtn.forEach((btn) => {
        // id = event.target.getAttribute('data-song-id'))
        btn.addEventListener("click", deleteSong());
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // const displayDuration = 4000;

    // function hideErrorMessage() {
    //     const errorContainer = document.getElementById('error-container');
    //     if (errorContainer) {
    //         errorContainer.style.display = 'none';
    //     }
    // }

    // const errorContainer = document.getElementById('error-container');
    // if (errorContainer) {
    //     const displayDuration = 4000;
    //     setTimeout(hideErrorMessage, displayDuration);
    // }

    let audio;
    const prev = document.querySelector('.prev');
    const next = document.querySelector('.next');
    let currentSongIndex = 0;
    var pause = document.querySelector('.pause');
    var play = document.querySelector('.play');
    const speakerBar = document.querySelector('.speaker-bar');
    const speaker = document.querySelector('.volume');
    const speakerContainer = document.querySelector('.speaker-container');
    const mute = document.querySelector('.mute');
    const progressBar = document.querySelector('.progress-bar');
    const progressContainer = document.querySelector('.progress-container');
    const startTime = document.querySelector('.start-time');
    const endTime = document.querySelector('.end-time');
    let songs = document.querySelectorAll('.song');
    let isLoopOn = false;
    let shuffleOn = false;
    const shuffleBtn = document.querySelector('.shuffle');
    const loopButton = document.querySelector('.loop');
    const name = document.querySelector('.name');
    const artist = document.querySelector('.artist');
    const songCoverImg = document.querySelector('.song-cover');
    let currentVolume = 0.5;
    const pauseIcon = document.querySelector('.pause_icon');
    const playIcon = document.querySelector('.play_icon');


    function getSongAttributes(song) {
        return {
            songUrl: song.getAttribute('data-song-url'),
            songName: song.getAttribute('data-song-name'),
            artistName: song.getAttribute('data-song-artist'),
            songCover: song.getAttribute('data-song-cover')
        };
    }
    
    songs.forEach((song, index) => {
        song.addEventListener('click', function () {
            songs.forEach((s) => {
                s.classList.remove('clicked');
            });

            song.classList.add('clicked');
    
            document.querySelector('.App__now-playing-bar').style.display = 'block';
            const { songUrl, songName, artistName, songCover } = getSongAttributes(song);
            const song_Id = song.getAttribute('data-song-id');
            currentSongIndex = index;
            playSong(songUrl, songName, artistName, songCover);
        });
    });
    
    function playNext() {
        console.log("Playing Next...");
        if (shuffleOn) {
            console.log("Shuffling...");
            const randomIndex = Math.floor(Math.random() * songs.length);
            const { songUrl, songName, artistName, songCover } = getSongAttributes(songs[randomIndex]);
            currentSongIndex = randomIndex;
            updateClickedClass();
            playSong(songUrl, songName, artistName, songCover);
        } else {
            currentSongIndex = (currentSongIndex + 1) % songs.length;
            const { songUrl, songName, artistName, songCover } = getSongAttributes(songs[currentSongIndex]);
            updateClickedClass();
            playSong(songUrl, songName, artistName, songCover);
        }
    }
    
    prev.addEventListener("click", function(){
        currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
        const { songUrl, songName, artistName, songCover } = getSongAttributes(songs[currentSongIndex]);
        updateClickedClass();
        playSong(songUrl, songName, artistName, songCover);
    });
    
    next.addEventListener("click", function(){
        playNext();
    });
    
    function updateClickedClass() {
        songs.forEach((s) => {
            s.classList.remove('clicked');
        });

        songs[currentSongIndex].classList.add('clicked');
    }

    shuffleBtn.addEventListener("click", function() {
    shuffleOn = !shuffleOn;
    if (shuffleOn) {
        console.log('Shuffle functionality activated');
        shuffleBtn.style.backgroundColor = 'yellow';
        shuffleBtn.style.borderRadius = '4px';
    } else {
        console.log('Loop functionality deactivated');
        shuffleBtn.style.backgroundColor = '';
        shuffleBtn.style.borderRadius = '';
    }
    });

function onSongEnd() {
    console.log("Song Ended");
    pause.style.display = 'none';
    play.style.display = 'block';
    if (!isLoopOn) {
        playNext();
    } else {
        audio.currentTime = 0;
        audio.play();
        pause.style.display = 'block';
        play.style.display = 'none';
    }
}

loopButton.addEventListener('click', function() {
    isLoopOn = !isLoopOn;
    if (isLoopOn) {
        console.log('Loop functionality activated');
        loopButton.style.backgroundColor = 'yellow';
        loopButton.style.borderRadius = '4px';
    } else {
        console.log('Loop functionality deactivated');
        loopButton.style.backgroundColor = '';
        loopButton.style.borderRadius = '';
    }
});
    function updateVolume(value) {
        currentVolume = value;
    }

    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${(seconds < 10 ? '0' : '')}${seconds}`;
    }

    function changeIcon(a) {
        if (playIcon || pauseIcon){
            if (a.paused) {
                playIcon.style.display = "block";
                pauseIcon.style.display = "none";
            } else {
                playIcon.style.display = "none";
                pauseIcon.style.display = "block";
            }
        }
    }

    let playing = false;

    if (playIcon){
        playIcon.onclick = function() {
            // playing = !playing;
            if (playing) {
                audio.play();
                changeIcon(audio);
                console.log("Resume");
                play.style.display = 'none';
                pause.style.display = 'block';
            } else {
                const { songUrl, songName, artistName, songCover } = getSongAttributes(songs[currentSongIndex]);
                const id = songs[currentSongIndex].getAttribute('data-song-id');
                songs[currentSongIndex].classList.add('clicked');
                likeHandlerZ(id);
                playSong(songUrl, songName, artistName, songCover);
                playing = true;
                play.style.display = 'none';
                pause.style.display = 'block';
                document.querySelector('.App__now-playing-bar').style.display = 'block';
                // changeIcon(audio);
                }
            }
    }
    if (pauseIcon){
        pauseIcon.onclick = function() {
            audio.pause();
            changeIcon(audio);
            play.style.display = 'block';
            pause.style.display = 'none';
        }
    }

    const menuMain = document.querySelector('.menu_main');
    // const menuNav = document.querySelector('.menu_nav');
    const navBar = document.querySelector('.App__nav-bar');
    const mainArea = document.querySelector('.App__main-view');

    menuMain.addEventListener('click', function() {
        navBar.style.left = '0';
    });
    // menuNav.addEventListener('click', function() {
    //     navBar.style.left = '-50%';
    // });
    mainArea.addEventListener('click', function() {
        navBar.style.left = '-50%';
    });
    document.querySelector('.App__now-playing-bar').addEventListener('click', function() {
        navBar.style.left = '-50%';
    });



    const lyricsButton = document.querySelector('.lyrics-button');
    const lyricsBar = document.querySelector('.lyrics-bar');

    lyricsButton.addEventListener('click', function() {
        console.log('btn clciked')
      if (lyricsBar.style.right === '-60%') {
        lyricsBar.style.right = '0';
      } else {
        lyricsBar.style.right = '-60%';
      }
    });



    function playSong(songUrl, songName, artistName, songCover) {
        console.log('Playing...');

        if (audio) {
            audio.pause();
            audio = null;
        }

        name.textContent = songName;
        artist.textContent = artistName;
        songCoverImg.src = songCover

        var lyricsBody = document.querySelector('.lyrics-body');
        var songArtist = document.querySelector('#artist');
        var title = document.querySelector('#title');

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrftoken },
            url: "/lyrics/",
            data: {
                'artist': artistName,
                'title': songName
            },
            dataType: 'json',
            success: function(response) {
                songArtist.textContent = response.Artist;
                title.textContent = response.Title;
                const lyricsLines = response.Lyrics.split('\n');
                lyricsBody.innerHTML = '';
                lyricsBody.innerHTML = response.Lyrics.replace(/\n/g, '<br>');
                // lyricsLines.forEach(line => {
                //     const p = document.createElement('p');
                //     p.textContent = line;
                //     lyricsBody.appendChild(p);
                // });
            },            
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

        const elementWithClickedClass = document.querySelector('.clicked');
        if (elementWithClickedClass) {
            clickedSongId = elementWithClickedClass.getAttribute('data-song-id');
            likeHandlerZ(clickedSongId);
        }
   
        audio = new Audio(songUrl);
        audio.volume = currentVolume;
        audio.play();
        playing = true;
        if (playIcon){
            changeIcon(audio);
        }
        audio.addEventListener('ended', onSongEnd);
        if (play.style.display === 'block') {
            play.style.display = 'none';
            pause.style.display = 'block';
        }

        
        play.onclick = function () {
            if (audio.paused) {
                play.style.display = 'none';
                pause.style.display = 'block';
                audio.play();
                changeIcon(audio);
            }
        };
    
        pause.onclick = function () {
            if (!audio.paused) {
                pause.style.display = 'none';
                play.style.display = 'block';
                audio.pause();
                changeIcon(audio);
            }
        };
    
        function updateSpeakerBar() {
            const volumePercentage = audio.volume * 100;
            speakerBar.style.width = `${volumePercentage}%`;
        }

        audio.addEventListener('volumechange', updateSpeakerBar);

        function updateProgressBar() {
            const progressPercentage = (audio.currentTime / audio.duration) * 100;
            progressBar.style.width = `${progressPercentage}%`;
            startTime.textContent = formatTime(audio.currentTime);
        }

        function seek(event) {
            const seekPosition = (event.offsetX / progressContainer.clientWidth) * audio.duration;
            audio.currentTime = seekPosition;
        }
        progressContainer.addEventListener('click', seek);

        function setEndTime() {
            endTime.textContent = formatTime(audio.duration);
        }

        function seekVol(event) {
            const seekPosVol = event.offsetX /speakerContainer.clientWidth;
            audio.volume = seekPosVol;
        }
        speakerContainer.addEventListener("click", seekVol);

        audio.addEventListener('timeupdate', updateProgressBar);
        audio.addEventListener('loadedmetadata', setEndTime);

        let previousVol;

        speaker.addEventListener("click", function(){
            speaker.style.display = "none";
            mute.style.display = "block";
            previousVol = audio.volume;
            audio.volume = 0.0;
        });
        mute.addEventListener("click", function() {
            speaker.style.display = "block";
            mute.style.display = "none";
            audio.volume = previousVol;
        });
    
        document.addEventListener('keydown', function (e) {
            if (e.code === 'Space') {
                if (audio.paused) {
                    // e.preventDefault();
                    console.log("<Space>");
                    audio.play();
                    pause.style.display = 'block';
                    play.style.display = 'none';
                    changeIcon(audio);
                } else {
                    audio.pause();
                    pause.style.display = 'none';
                    play.style.display = 'block';
                    changeIcon(audio);
                }
            } else if (e.key === 'ArrowLeft') {
                console.log("<Left>");
                if (audio.currentTime >= 10) {
                    audio.currentTime -= 10;
                } else {
                    audio.currentTime = 0;
                }
            } else if (e.key === 'ArrowRight') {
                console.log("<Right>");
                if (audio.currentTime + 10 <= audio.duration) {
                    audio.currentTime += 10;
                } else {
                    audio.currentTime = audio.duration;
                }
            }
            else if (e.key === 'ArrowUp') {
                console.log("<Up>");
                if (audio.volume < 1.0) {
                    if (audio.volume + 0.05 > 1.0) {
                        audio.volume = 1.0;
                    } else {
                        audio.volume += 0.05;
                        if (audio.volume > 0.01) {
                            speaker.style.display = 'block';
                            mute.style.display = 'none';
                        }
                    }
                    updateVolume(audio.volume);
                }
            } else if (e.key === 'ArrowDown') {
                console.log("<Down>");
                if (audio.volume > 0.0) {
                    if (audio.volume - 0.05 < 0.0) {
                        audio.volume = 0.0;
                    } else {
                        audio.volume -= 0.05;
                        if (audio.volume < 0.1) {
                            audio.volume = 0;
                            speaker.style.display = 'none';
                            mute.style.display = 'block';
                        }
                    }
                    updateVolume(audio.volume);
                }
            }
        });
    } 
    window.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            return false;
        }
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp'){e.preventDefault(); return false;}
    });
});
