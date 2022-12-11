# Guess Who?

### An online version of classic table game - "guess who?"

Two players

![Front](https://github.com/issdn/guesswho/blob/master/images/1.png)

![Lobby](https://github.com/issdn/guesswho/blob/master/images/2.png)

Pick your character

![Picking](https://github.com/issdn/guesswho/blob/master/images/3.png)

Ask questions

![Asking](https://github.com/issdn/guesswho/blob/master/images/4.png)

Answer

![Answer](https://github.com/issdn/guesswho/blob/master/images/6.png)

![Win](https://github.com/issdn/guesswho/blob/master/images/5.png)

# How to run (Only tested on windows)

Prep: Images of the characters I generated with help of [stylegen3](https://github.com/NVlabs/stylegan3) then put inside `server/src/characters` then scaled down to 128x128 with the script `resize_images()` inside file `server/src/image_manipulation.py`.
You either have to generate them yourself, get different ones or download my images from [this link](https://drive.google.com/drive/folders/1W6Ib8meI1NBFotr9Echt3OLC0mn5wCXe?usp=sharing).
Finally, put them `server/src/characters` and go to the next step.

## Through Docker

1. [Download Docker](https://docs.docker.com/desktop/install/windows-install/)

### docker-compose for the server and the client

2. In source directory run: `docker compose up`
3. Server and client should be running. Open `localhost:4173/` in the browser.

### docker for the client or the server or both

- server: Inside `guesswho/server` run `docker build -t server .` and then `docker run -p 80:80 server`.

- client: Inside `guesswho/client` run `docker build -t client .` and then `docker run -p 4173:4173 server`.

## No docker

1. Install python, node + npm
2. Inside `guesswho/server` run:

   - `python -m venv env`
   - `env\Sripts\activate`
   - `pip install -r requirements.txt`
   - `uvicorn main:app --host 0.0.0.0 --port 80`

3. Inside `guesswho/client` run:

   - `npm install`
   - `npm run build`
   - `npm run preview`

   or for development

   - `npm install`
   - `npm run dev`

---

### My windows termina config for dev:

```
{
    "guid": "{407bae8a-dc67-449a-9e80-9361be0382d2}",
    "hidden": false,
    "name": "guesswhoClient",
    "startingDirectory": "E:\\guesswho\\client",
    "tabTitle": "guesswho_client",
    "commandline": "powershell.exe -NoExit \"npm run dev\""
},
{
    "guid": "{c8c1b4ea-4e5a-448e-a439-7cf1e0fd79a6}",
    "hidden": false,
    "name": "guesswhoServer",
    "startingDirectory": "E:\\guesswho\\server",
    "tabTitle": "guesswho_server",
    "commandline": "powershell.exe -NoExit \"cd src; .\\env\\Scripts\\activate;  uvicorn main:app --reload\""
},
```

### Commmand that i ran inside wsl 2 to generate images with stylegen3:

For loop, where 50..250 is the range of numbers of images to generate which is also used as a seed for stylegen.

```
for i in {50..250}; do docker run --gpus all -it --rm --user $(id -u):$(id -g) -v `pwd`:/scratch --workdir /scratch -e HOME=/scratch stylegan3 python gen_images.py --outdir=out --trunc=1 --seeds=$i --network=https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-metfaces-1024x1024.pkl; done
```
