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

    const songs = document.querySelectorAll('.song');
    songs.forEach((song, index) => {
        song.addEventListener('click', function () {
            document.querySelector('.App__now-playing-bar').style.display = 'block';
            const songUrl = song.getAttribute('data-song-url');
            currentSongIndex = index;
            playSong(songUrl);
        });
    });

    prev.addEventListener("click", function(){
        currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
        const previousSongUrl = songs[currentSongIndex].getAttribute('data-song-url');
        playSong(previousSongUrl);
    })
    next.addEventListener("click", function(){
        songUrl = songs[(currentSongIndex + 1) % songs.length ].getAttribute('data-song-url');
        playSong(songUrl);
    })
    
    function playSong(songUrl) {
        console.log('Playing...');
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

        if (audio) {
            audio.pause();
            audio = null;
        }
    
        audio = new Audio(songUrl);
        audio.play();
    
        if (play.style.display === 'block') {
            play.style.display = 'none';
            pause.style.display = 'block';
        }
    
        play.onclick = function () {
            if (audio.paused) {
                play.style.display = 'none';
                pause.style.display = 'block';
                audio.play();
            }
        };
    
        pause.onclick = function () {
            if (!audio.paused) {
                pause.style.display = 'none';
                play.style.display = 'block';
                audio.pause();
            }
        };
    
        audio.addEventListener('ended', function () {
            pause.style.display = 'none';
            play.style.display = 'block';
        });
        function updateSpeakerBar() {
            const volumePercentage = audio.volume * 100;
            speakerBar.style.width = `${volumePercentage}%`;
        }

        audio.addEventListener('volumechange', updateSpeakerBar);
    
        function formatTime(time) {
            const minutes = Math.floor(time / 60);
            const seconds = Math.floor(time % 60);
            return `${minutes}:${(seconds < 10 ? '0' : '')}${seconds}`;
        }

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
                } else {
                    audio.pause();
                    pause.style.display = 'none';
                    play.style.display = 'block';
                }
            } else if (e.key === 'ArrowLeft') {
                if (audio.currentTime >= 10) {
                    audio.currentTime -= 10;
                } else {
                    audio.currentTime = 0;
                }
            } else if (e.key === 'ArrowRight') {
                if (audio.currentTime <= audio.duration - 10) {
                    audio.currentTime += 10;
                } else {
                    audio.currentTime = audio.duration;
                }
            } else if (e.key === 'ArrowUp') {
                if (audio.volume < 1.0) {
                    audio.volume += 0.05;
                    if (audio.volume > 0.01) {
                        speaker.style.display = "block";
                        mute.style.display = "none";
                    }
                }
            } else if (e.key === 'ArrowDown') {
                if (audio.volume > 0.0) {
                    audio.volume -= 0.05;
                        if (audio.volume < 0.1){
                            audio.volume = 0;
                            speaker.style.display = "none";
                            mute.style.display = "block";
                        }
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
