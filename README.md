<div align="center">
<img width="30%" src="./static/images/Logo-new.png">
 
# TrackTonic
</div>

## **TrackTonic**

TrackTonic is a music streaming website crafted with Django, designed for simplicity and built as a personal project for learning purposes. This endeavor allowed me to delve into the intricacies of web development and gain hands-on experience with Django, HTML, CSS, and JavaScript.

## Features

### User-Friendly Interface
The clean and intuitive interface ensures a seamless experience for users, making music streaming a delight.

### Personal Playlist Creation

Users can create playlists by uploading music from their devices. Simply navigate to the playlist creation section and select the songs you want to add to your playlist.

### Metadata Extraction

The app automatically extracts metadata from the uploaded music files to populate song object fields. This ensures that all the necessary information about the songs is available for easy organization and searching ensuring a hassle-free music library management.

### Lyrics Display

Integrated with the Genius API, TrackTonic lets users explore song lyrics effortlessly while enjoying their favorite tunes.Simply click on the lyrics icon next to the song to display the lyrics in a separate section.
 

### Download Functionality

Download individual songs or entire playlists (in zip format) shared by other users to broaden your musical horizon.
Simply navigate to the playlist you want to download and click on the download button.

## Local Setup

To set up the project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/Nathaniel81/TrackTonic.git`
2. Install the necessary dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

Make sure you have Python and Django installed on your machine before proceeding with the above steps.

## Docker Setup

To run TrackTonic using Docker, you can use the provided Dockerfile and docker-compose.yml files in the project's root directory. Follow these steps:

1. Build the Docker images: `docker-compose build`
2. Run the Docker containers: `docker-compose up`

The application will be accessible at http://localhost:8000/ in your web browser.

## External APIs

TrackTonic seamlessly integrates with the Genius API to retrieve song lyrics. To enable this feature, follow these steps:

1. **Get Your Genius API Key:**
   - Visit the [Genius API Documentation](https://docs.genius.com/) and sign up for an API key.
   - Once registered, you will receive a unique API key that allows TrackTonic to access the Genius API.

2. **Create a Configuration File:**
   - In the project's root directory, create a `.env` file if one doesn't exist.

3. **Store Your API Key:**
   - Open the `.env` file and add the following line, replacing `[YOUR_GENIUS_API_KEY]` with the key you obtained:
     ```plaintext
     GENIUS_API_KEY=[YOUR_GENIUS_API_KEY]
     ```

4. **Configure the Application:**
   - The TrackTonic application is designed to read the Genius API key from the `.env` file during runtime.
   - With the API key in place, TrackTonic can dynamically fetch and display lyrics for the songs being played.

By following these steps, you ensure that TrackTonic has the necessary authorization to access the Genius API and enrich your music streaming experience with on-the-fly song lyrics.

## Learning Journey:

This project is more than just a music streaming app; it's a product of my journey into web development. Built with a focus on practical learning, TrackTonic showcases the skills and insights gained during the development process. From setting up Django models to handling user authentication and integrating external APIs, every line of code represents a step forward in my coding proficiency.

## Why TrackTonic?

The name TrackTonic reflects the harmony of tracks and the invigorating essence of learning. It's not just a music streaming website; it's a testament to the power of hands-on experience and continuous improvement.

Feel free to explore TrackTonic, and join me in this musical and coding journey!

## App Preview :

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
  
</p>
<img src="">
</td> 
<td width="50%">
<br>
<p align="center">
  
</p>
<img src="">  
</td>
</table>
