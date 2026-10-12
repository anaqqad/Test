# "Sign in the Dark" reel (book 5, ch. "Lights Out")

Scene: at the gallery gala the lights go out, UV floods reveal Mara's hidden signatures under the varnish of
all 31 paintings that her husband sold under his mistress's name, and her dying mother's last words.

On the PC (Noor&Baba folder, see HOWTO_Seedance_Kindle.md):
    python seedance.py prompt.txt out.mp4 cover.png --seconds 20 --size 480x854     (~$2)
    bash append_endcard.sh out.mp4 final.mp4

Files: prompt.txt, cover.png (Image 1), kindle_endcard.png/.mp4 (3 s end card), make_endcard.py
(rebuild the card for another cover: python make_endcard.py COVER Cinzel.ttf 1f4da.png 1f447.png out.png).
After posting, pin the first comment: "📚 My books on Amazon Kindle: <your Amazon link>".
