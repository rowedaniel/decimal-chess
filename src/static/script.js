let get_tile = function(row, col, index)
{
    row += 1;
    col += 1;
    return document.querySelector(`tr:nth-child(${row}) td:nth-child(${col})`);
}

let do_on_all_tiles = function(func)
{
    for(let row = 0; row < 8; ++row) {
        for(let col = 0; col < 8; ++col) {
            let tile = get_tile(row, col, 0);
            if(!tile) { continue; }

            func(row, col, 0, tile);
        }
    }
}
let clear_tile_markings = function()
{
    do_on_all_tiles(function(row, col, i, tile) {
        tile.classList.remove("movable");
    });
}


window.addEventListener("DOMContentLoaded", function(event) {

    const socket = io();

    socket.on("r_update_pieces", function(data) {
        for(let key in data) {
            let keyparts = key.split(',');
            let row = parseInt(keyparts[0]);
            let col = parseInt(keyparts[1]);

            let object = get_tile(row, col, 0);
            if(!object) { continue; }
            for(let c of data[key]) {
                object.classList.add(c);
            }
        }
    });

    socket.on("r_view", function(data) {
        clear_tile_markings();
        for(let loc of data) {
            let tile = get_tile(loc[0], loc[1], loc[2]);
            if(!tile) { console.log("hmm", loc[0], loc[1]); continue; }
            tile.classList.add("movable");
        }
    });


    do_on_all_tiles(function(row, col, index, tile) {
        tile.addEventListener("mouseover", function(event) {
            socket.emit('q_view', {'row': row, 'col': col, 'index':0});
            console.log("getting tile:", row, col);
        });
    });

});

