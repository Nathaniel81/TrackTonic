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
    const displayDuration = 4000;

    function hideErrorMessage() {
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) {
            errorContainer.style.display = 'none';
        }
    }

    const errorContainer = document.getElementById('error-container');
    if (errorContainer) {
        const displayDuration = 4000;
        setTimeout(hideErrorMessage, displayDuration);
    }

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
    const songs = document.querySelectorAll('.song');
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
            // Remove the 'clicked' class from all songs
            songs.forEach((s) => {
                s.classList.remove('clicked');
            });
    
            // Add the 'clicked' class to the clicked song
            song.classList.add('clicked');
    
            document.querySelector('.App__now-playing-bar').style.display = 'block';
            const { songUrl, songName, artistName, songCover } = getSongAttributes(song);
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
        // Remove the 'clicked' class from all songs
        songs.forEach((s) => {
            s.classList.remove('clicked');
        });
    
        // Add the 'clicked' class to the current song
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

// function loopHandler() {
//     if (isLoopOn) {
//         play.style.display = 'none';
//         pause.style.display = 'block';
//         audio.currentTime = 0;
//         audio.play();
//     }
// }

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
        if (a.paused) {
            playIcon.style.display = "block";
            pauseIcon.style.display = "none";
        } else {
            playIcon.style.display = "none";
            pauseIcon.style.display = "block";
        }
    }

    let playing = false;

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
            playSong(songUrl, songName, artistName, songCover);
            playing = true;
            play.style.display = 'none';
            pause.style.display = 'block';
            document.querySelector('.App__now-playing-bar').style.display = 'block';
            // changeIcon(audio);
        }
    }
    pauseIcon.onclick = function() {
        audio.pause();
        changeIcon(audio);
        play.style.display = 'block';
        pause.style.display = 'none';
    }


    function playSong(songUrl, songName, artistName, songCover) {
        console.log('Playing...');
        

        if (audio) {
            audio.pause();
            audio = null;
        }

        name.textContent = songName;
        artist.textContent = artistName;
        songCoverImg.src = songCover
        
        audio = new Audio(songUrl);
        audio.volume = currentVolume;
        audio.play();
        playing = true;
        changeIcon(audio);
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
                if (audio.currentTime >= 10) {
                    audio.currentTime -= 10;
                } else {
                    audio.currentTime = 0;
                }
            } else if (e.key === 'ArrowRight') {
                if (audio.currentTime + 10 <= audio.duration) {
                    audio.currentTime += 10;
                } else {
                    audio.currentTime = audio.duration;
                }
            }
            else if (e.key === 'ArrowUp') {
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
