# Meme Generator

Aplikacija omogoča nalaganje slike preko spletnega vmesnika, vnos zgornjega in spodnjega besedila, generiranje nove slike z dodanim tekstom ter prikaz ustvarjenega mema v brskalniku.  
Projekt je izdelan v jeziku Python z ogrodjem Flask in knjižnico Pillow za obdelavo slik. Aplikacija je dockerizirana in se izvaja znotraj Docker kontejnerja.

---

## Tehnologije

- Python 3.13
- Flask
- Pillow
- Docker

---

## Navodila za zagon z Dockerjem

### 1. Gradnja Docker slike

V mapi, kjer se nahajata datoteki `app.py` in `Dockerfile`, izvedemo ukaza:

```bash
docker build -t meme-generator .

docker run --rm -d --name meme-gen -p 5000:5000 meme-generator
```


