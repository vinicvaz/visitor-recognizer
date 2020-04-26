<p align="center">
  <img width="300" src="https://i.imgur.com/mnjSnZg.png">
  <p align="center"><strong>Web app with facial recognition running on a client-server architeture</strong> </p>
  
</p>


## Description
The app will provide to the user the possibility of using a web facial recognition and customer control system. Just perform a registration and login and you can use the application for various purposes, such as security, personalized customer service, among others.

## Technical Description
When logged the clients can start streaming their webcams to the server, this data will be encoded in base64 format and sended over sockets, the server will get the frames, process it and return to the client the information of the detecteds faces.

## Mainly Technologies

* Flask
* OpenCV and OpenCV.js
* JS
* Python

## Dependencies
All dependencies are in the **requirements.txt** file
```
pip install -r requirements.txt
```
## Visuals

<h2 align="center" styles="font-size:bold">Images</h2>
<p align="center">
  <img width="780" src="https://i.imgur.com/ACRfOnI.png">
   <img  width="780" src="https://i.imgur.com/4FCG1Rd.png">
  <img  width="780" src="https://i.imgur.com/9vxH6hM.png">
  <img width="780" src="https://i.imgur.com/VavfkdM.png">
</p>


<h2 align="center" styles="font-size:bold">Watch a video demo (audio in portugues for while)</h2>

[![Watch the video](https://i.imgur.com/NLit6Zj.png)](
https://www.youtube.com/watch?v=hsFuOOqj3WQ&feature=youtu.be)


## License
[APACHE](https://github.com/vinicvaz/visitor-recognizer/blob/dev/LICENSE.md)
