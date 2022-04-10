G_PAINTINGS_URL_BASE = location.protocol + '//' + location.hostname + ':' + location.port;
G_PAINTINGS_BY_ID_API_URL = G_PAINTINGS_URL_BASE + '/api/paintings/';

g_current_painting = null;

class Painting
{
    constructor (painting_id,
                 title,
                 artist,
                 date,
                 date_selected,
                 image_link,
                 paintings_by_id_map)
    {
        this.id = parseInt(painting_id);
        this.title = title;
        this.artist = artist;
        this.date = date;
        this.date_selected = date_selected;
        this.image_link = image_link;

        this.paintings_by_id_map = paintings_by_id_map;
        this.paintings_by_id_map[this.id] = this;

        this.next_painting = null;
        this.prev_painting = null;
    }

    async display ()
    {
        if (!this._painting_info_set())
            await this._fetch()

        if (!this.next_painting)
            await this._fetch_next_painting();

        if (!this.prev_painting)
            await this._fetch_prev_painting();

        let painting_id_elem = document.getElementById('painting_id');
        painting_id_elem.setAttribute('data-id', this.id);

        let painting_title_elem = document.getElementById('painting_title');
        painting_title_elem.innerHTML = this.title;

        let painting_artist_elem = document.getElementById('painting_artist');
        painting_artist_elem.innerHTML = 'by ' + this.artist;

        let painting_date_elem = document.getElementById('painting_date');
        painting_date_elem.innerHTML = this.date;

        let painting_date_selected_elem = document.getElementById('painting_date_selected');
        painting_date_selected_elem.innerHTML = this.date_selected;

        let painting_image_elem = document.getElementById('painting_image');
        let image = document.createElement("img");
        image.src = this.image_link;
        painting_image_elem.appendChild(image);

        this._display_arrows();

        g_current_painting = this;
    }

    display_next_painting ()
    {
        this.next_painting.display();
    }

    display_prev_painting ()
    {
        this.prev_painting.display();
    }

    _display_arrows ()
    {
        let next_arrow = document.getElementById('next_painting_arrow');
        let prev_arrow = document.getElementById('prev_painting_arrow');

        if (this.next_painting)
        {
            next_arrow.classList.add('painting_arrow_hoverable');
            next_arrow.classList.remove('painting_arrow_not_hoverable');
        }
        else
        {
            next_arrow.classList.add('painting_arrow_not_hoverable');
            next_arrow.classList.remove('painting_arrow_hoverable');
        }

        if (this.prev_painting)
        {
            prev_arrow.classList.add('painting_arrow_hoverable');
            prev_arrow.classList.remove('painting_arrow_not_hoverable');
        }
        else
        {
            prev_arrow.classList.add('painting_arrow_not_hoverable');
            prev_arrow.classList.remove('painting_arrow_hoverable');
        }
    }

    _painting_info_set ()
    {
        return this.title &&
               this.artist &&
               this.date &&
               this.date_selected &&
               this.image_link;
    }

    async _fetch ()
    {
        let response = await fetch(G_PAINTINGS_BY_ID_API_URL + this.id + '/');

        if (!response.ok)
            return;

        let data = await response.json();

        this.title = data['title'];
        this.artist = data['artist'];
        this.date = data['date'];
        this.date_selected = data['date_selected'];
        this.image_link = data['image_link'];
    }

    async _fetch_next_painting ()
    {
        let next_id = this.id + 1;

        if (next_id in this.paintings_by_id_map)
        {
            this.next_painting = this.paintings_by_id_map[next_id];
            return;
        }

        let response = await fetch(G_PAINTINGS_BY_ID_API_URL + next_id + '/');

        if (!response.ok)
            return;

        let data = await response.json();

        this.next_painting = new Painting(next_id,
                                          data['title'],
                                          data['artist'],
                                          data['date'],
                                          data['date_selected'],
                                          data['image_link'],
                                          this.paintings_by_id_map);
    }

    async _fetch_prev_painting ()
    {
        let prev_id = this.id - 1;

        if (prev_id <= 0)
            return;

        if (prev_id in this.paintings_by_id_map)
        {
            this.prev_painting = this.paintings_by_id_map[prev_id];
            return;
        }

        let response = await fetch(G_PAINTINGS_BY_ID_API_URL + prev_id + '/');

        if (!response.ok)
            return;

        let data = await response.json();

        this.prev_painting = new Painting(prev_id,
                                          data['title'],
                                          data['artist'],
                                          data['date'],
                                          data['date_selected'],
                                          data['image_link'],
                                          this.paintings_by_id_map);
    }
}

(function () {

    let painting_id_elem = document.getElementById('painting_id');
    let starting_painting_id = painting_id_elem.getAttribute('data-id');
    let next_arrow = document.getElementById('next_painting_arrow');
    let prev_arrow = document.getElementById('prev_painting_arrow');

    let paintings_by_id_map = {};

    let starting_painting = new Painting(starting_painting_id,
                                         null,
                                         null,
                                         null,
                                         null,
                                         null,
                                         paintings_by_id_map);

    starting_painting.display();

    next_arrow.addEventListener('click', function (event) {
        g_current_painting.display_next_painting();
    });

    prev_arrow.addEventListener('click', function (event) {
        g_current_painting.display_prev_painting();
    });

})();

